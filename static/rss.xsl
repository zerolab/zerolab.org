<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="3.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:atom="http://www.w3.org/2005/Atom" xmlns:dc="http://purl.org/dc/elements/1.1/"
                xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
  <xsl:output method="html" version="1.0" encoding="UTF-8" indent="yes"/>
  <xsl:template match="/">
    <html lang="en">
      <head>
        <title><xsl:value-of select="/rss/channel/title"/> Web Feed</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1"/>
        <link rel="stylesheet" href="css/main.min.css"/>
      </head>
      <body>
        <header role="banner" class="header wrapper">
          <div class="warning warning--label">
            <h2 class="warning__label">Note</h2>
            <strong>This is a web feed,</strong> also known as an RSS feed. <strong>Subscribe</strong> by copying the URL from the address bar into your newsreader.
          </div>

          <p>
            Visit <a href="https://aboutfeeds.com">About Feeds</a> to get started with newsreaders and subscribing. It’s free.
          </p>
        </header>
        <main id="main">
          <article class="flow wrapper">
            <header class="simple">
              <h1>
                <!-- https://www.svgrepo.com/svg/25140/rss -->
                <svg xmlns="http://www.w3.org/2000/svg" xml:space="preserve" viewBox="0 0 455.731 455.731" style="width: 1.2em; height: 1.2em; vertical-align: text-bottom;"><path d="M0 0h455.731v455.731H0z" style="fill:#f78422"/><path d="M296.208 159.16C234.445 97.397 152.266 63.382 64.81 63.382v64.348c70.268 0 136.288 27.321 185.898 76.931 49.609 49.61 76.931 115.63 76.931 185.898h64.348c-.001-87.456-34.016-169.636-95.779-231.399z" style="fill:#fff"/><path d="M64.143 172.273v64.348c84.881 0 153.938 69.056 153.938 153.939h64.348c0-120.364-97.922-218.287-218.286-218.287z" style="fill:#fff"/><circle cx="109.833" cy="346.26" r="46.088" style="fill:#fff"/></svg>

                Web feed preview for "<xsl:value-of select="/rss/channel/title"/>"
              </h1>
              <div class="post__meta">
                <p><xsl:value-of select="/rss/channel/description"/></p>
                <a class="head_link" target="_blank">
                  <xsl:attribute name="href">
                    <xsl:value-of select="/rss/channel/link"/>
                  </xsl:attribute>
                  Visit website &#x2192;
                </a>
              </div>
            </header>
            
            <h2>Recent items</h2>
            <xsl:for-each select="/rss/channel/item">
              <div class="pb-5">
                <h3 class="mb-0">
                  <a target="_blank">
                    <xsl:attribute name="href">
                      <xsl:value-of select="link"/>
                    </xsl:attribute>
                    <xsl:value-of select="title"/>
                  </a>
                </h3>
                <small class="text-gray">
                  Published: <xsl:value-of select="pubDate" />
                </small>
              </div>
            </xsl:for-each>
          </article>
        </main>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>
