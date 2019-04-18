# coding:utf-8
import scrapy


class TkSpider(scrapy.Spider):
    name = "tkspider"

    def start_requests(self):
        url = getattr(self, 'url', None)
        if url is not None:
            url = url
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        if self.parent_selector:
            for data in response.css(self.parent_selector):
                # Call custom generator of selector
                yield self._selector_generator(data)
                # self.log('Saved %s' % data)
            if self.pagination != "":
                next_page = response.css(self.pagination).get()
                if next_page is not None:
                    yield response.follow(next_page, self.parse)

    def _selector_generator(self, data):
        """
        Custom generator for display all selectors
        :param data: All selectors response
        :return: yield generator dictionary
        """
        if self.selectors:
            # Call method parse_entry_to_dict for transform str to dictionary
            selector_dict = TkSpider.parse_entry_to_dict(self.selectors)
            selector_dict_content = dict()

            for s_key, s_value in selector_dict.items():
                if data.css(s_value) and data.css(s_value).get() != " ":
                    selector_dict_content[s_key] = data.css(s_value).get()
                    print("----", selector_dict_content[s_key])
            return selector_dict_content

    @staticmethod
    def parse_entry_to_dict(entries):
        """
        Transform string entry to dictionary
        :param entries: str entries texte format
        :return: dict entries_dict
        """
        try:
            entries_dict = (dict(entry.split("|") for entry in entries.split("\n") if entry))
            return entries_dict
        except ValueError:
            raise
