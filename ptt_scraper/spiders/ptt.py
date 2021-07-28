import scrapy



class PTTSpider(scrapy.Spider):
    name = 'ptt'
    allowed_domains = ['www.ptt.cc']
    start_urls = ['https://www.ptt.cc/bbs/NBA/index.html']
    page_cnt = 0
    def parse(self, response):
        
        post_title_links = response.xpath("//div[@class='r-ent']/div[@class='title']/a")
        
        for post_title_link in post_title_links:
            yield self.scrape_post_from_link(post_title_link)
        self.page_cnt += 1
        if self.page_cnt < 10:
            next_page_url = "https://www.ptt.cc/" + response.xpath("//div[@class='btn-group btn-group-paging']/a/@href").getall()[1]

            yield scrapy.Request(next_page_url, callback=self.parse)
        
    def scrape_post_from_link(self, post_title_link):
        title = post_title_link.xpath("../../div[@class='title']/a/text()").get()
        author = post_title_link.xpath("../../div[@class='meta']/div[@class='author']/text()").get()
        
        push_text = post_title_link.xpath("../../div[@class='nrec']/span/text()").get()
        if push_text == "爆":
            push = 100
        elif push_text == None:
            push = 0
        elif push_text.isdigit():
            push = int(push_text)
        else:
            push = 0
        item = {
            "title": title,
            "author": author,
            "push": push
        }

        post_url = "https://www.ptt.cc/" + post_title_link.xpath("@href").get()
        return scrapy.Request(post_url, callback=self.parse_post, cb_kwargs=dict(item = item))
    def parse_post(self, response, item):
        
        comments = response.xpath("//div[@class='push']/span[@class='f3 push-content']/text()").getall()
        comments = list(map(lambda x:x[2:], comments))
        comments = ('\n').join(comments)
        item['comments'] = comments

        #print(item)
        return item
        
        

