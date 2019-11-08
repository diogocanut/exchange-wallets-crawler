# -*- coding: utf-8 -*-
import scrapy


class WalletsSpider(scrapy.Spider):
    name = 'wallets'
    allowed_domains = ['walletexplorer.com']
    start_urls = ['http://walletexplorer.com/']
    global wallets
    gwallet = ''

    def parse(self, response):
        r = response.xpath('//table/tr/td/ul/li/a/@href').extract()[:30]
        self.wallets = r
        for wallet in r:
            for page in range(0,20):
                next_page = response.urljoin(str(wallet) + '?page={0}'.format(page))
                self.gwallet = wallet
                yield scrapy.Request(next_page, callback=self.parse_wallets)

    def parse_wallets(self, response):
        page_transactions = response.xpath('//table/tr')
        # page_transactions = response.xpath('//table/tr/td/a/@href').extract()
        for full_transaction in page_transactions:
            transaction = full_transaction.xpath('td/a/@href').extract_first()
            if transaction in self.wallets:
                tx = transaction.split('/')[-1]
                wl = self.gwallet.split('/')[-1]
                amount = full_transaction.css('.amount::text').get().replace('\xa0','')
                print(tx + "  ---  " + wl + "  --- " + amount)
                yield {'wallet1': tx, 'wallet2': wl, 'amount': amount}



