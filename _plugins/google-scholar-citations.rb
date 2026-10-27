module Jekyll
    class GoogleScholarCitationsTag < Liquid::Tag
        def initialize(tag_name, params, tokens)
            super
            splitted = params.split(" ").map(&:strip)
            @scholar_id = splitted[0]
            @article_id = splitted[1]
        end

        def render(context)
            article_id = context[@article_id].to_s
            scholar_id = context[@scholar_id].to_s
            snapshot = context.registers[:site].data['google_scholar_citations']
            return 'N/A' unless snapshot.is_a?(Hash) && snapshot['scholar_userid'] == scholar_id

            publication = snapshot.fetch('publications', {})[article_id]
            count = publication && publication['citations']
            # No network requests during rendering. Unknown counts stay unknown;
            # valid zero counts remain distinct from an unavailable provider.
            count.is_a?(Integer) && count >= 0 ? count.to_s : 'N/A'
        end
    end
end

Liquid::Template.register_tag('google_scholar_citations', Jekyll::GoogleScholarCitationsTag)
