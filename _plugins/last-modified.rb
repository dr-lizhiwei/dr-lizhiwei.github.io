require 'open3'
require 'time'

# Preserve the sitemap's URL set. Only supply content modification timestamps,
# based on version history rather than the time of every site build.
Jekyll::Hooks.register :site, :pre_render do |site|
  output, status = Open3.capture2('git', '-C', site.source, 'log', '--format=DATE:%cI', '--name-only', '--', '_pages', '_posts', '_news', '_projects', 'news.html')
  next unless status.success?

  modified = {}
  timestamp = nil
  output.each_line do |line|
    line = line.strip
    if line.start_with?('DATE:')
      timestamp = line.delete_prefix('DATE:')
    elsif timestamp && !line.empty?
      modified[line] ||= timestamp
    end
  end
  explicit_page_dates = site.pages.select { |page| page.data['last_modified_at'] }.map(&:object_id)
  documents = site.collections.values.flat_map(&:docs) + site.pages
  documents.each do |document|
    next if document.data['last_modified_at']

    relative = document.path.to_s.tr('\\', '/').delete_prefix(site.source.tr('\\', '/').sub(%r{/\z}, '') + '/')
    document.data['last_modified_at'] = modified[relative] if modified[relative]
  end
  site.pages.each do |page|
    next if explicit_page_dates.include?(page.object_id)

    posts = if page.respond_to?(:posts)
              page.posts # jekyll-archives stores posts as an attribute, outside data.
            elsif page.url == '/news/'
              site.collections['news']&.docs
            elsif page.data.dig('pagination', 'enabled')
              site.posts.docs
            end
    next unless posts

    dates = posts.map { |post| post.data['last_modified_at'] || post.date }
    dates << page.data['last_modified_at']
    # Pagination pages copy front matter but lose the source page's path.
    dates << modified['_pages/blog.md'] if page.data.dig('pagination', 'enabled')
    dates.compact!
    page.data['last_modified_at'] = dates.max_by { |date| Time.parse(date.to_s) } unless dates.empty?
  end
rescue Errno::ENOENT
  Jekyll.logger.warn 'Sitemap:', 'Git is unavailable; using existing content dates.'
end
