require 'uri'

module Jekyll
  module LocalImageDimensions
    # Read local image headers without requiring ImageMagick or another gem.
    def image_dimensions(input)
      return [] if input.to_s.empty? || input.to_s.include?('://')

      site = @context.registers[:site]
      relative = URI::DEFAULT_PARSER.unescape(input.to_s.split(/[?#]/).first).sub(%r{\A/}, '')
      path = File.expand_path(relative, site.source)
      return [] unless path.start_with?(File.expand_path(site.source) + File::SEPARATOR) && File.file?(path)

      cache = site.instance_variable_get(:@local_image_dimensions) || {}
      site.instance_variable_set(:@local_image_dimensions, cache)
      cache[path] ||= read_image_dimensions(path)
    end

    private

    def read_image_dimensions(path)
      File.open(path, 'rb') do |file|
        header = file.read(32).to_s
        return header[16, 8].unpack('NN') if header.start_with?("\x89PNG\r\n\x1a\n".b)
        return header[6, 4].unpack('vv') if header.start_with?('GIF87a', 'GIF89a')
        if header.start_with?('RIFF') && header[8, 4] == 'WEBP' && header[12, 4] == 'VP8X'
          width = header[24, 3].unpack('C3').each_with_index.sum { |byte, index| byte << (8 * index) } + 1
          height = header[27, 3].unpack('C3').each_with_index.sum { |byte, index| byte << (8 * index) } + 1
          return [width, height]
        end
        return [] unless header.start_with?("\xff\xd8".b)

        file.seek(2)
        until file.eof?
          byte = file.read(1)
          next unless byte == "\xff".b

          marker = file.read(1)
          marker = file.read(1) while marker == "\xff".b
          break unless marker
          code = marker.unpack1('C')
          next if code == 0x01 || (0xd0..0xd8).cover?(code)
          break if [0xd9, 0xda].include?(code)

          length = file.read(2).to_s.unpack1('n')
          break unless length && length >= 2
          if [0xc0, 0xc1, 0xc2, 0xc3, 0xc5, 0xc6, 0xc7, 0xc9, 0xca, 0xcb, 0xcd, 0xce, 0xcf].include?(code)
            return file.read(5)[1, 4].unpack('nn').reverse
          end
          file.seek(length - 2, IO::SEEK_CUR)
        end
      end
      []
    rescue IOError, SystemCallError, TypeError, NoMethodError
      []
    end
  end
end

Liquid::Template.register_filter(Jekyll::LocalImageDimensions)
