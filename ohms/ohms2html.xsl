<?xml version="1.0"?>

<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:o="https://www.weareavp.com/nunncenter/ohms">
  <xsl:output method="html" encoding="utf8"/>
  <xsl:template match="/o:ROOT/o:record">
    <html>
      <head>
        <title><xsl:value-of select="o:title"/></title>
        <link rel="stylesheet" href="ohms.css"/>
      </head>
      <body>
        <h1><xsl:value-of select="o:title"/></h1>
        <audio controls="controls"><xsl:attribute name="src"><xsl:value-of select="o:media_url"/></xsl:attribute></audio>
        <dl class="record">
          <xsl:choose>
            <xsl:when test="o:date/@value/text()">
              <dt>Recorded</dt><dd><xsl:value-of select="o:date/@value"/></dd>
            </xsl:when>
            <xsl:when test="o:date_nonpreferred_format/text()">
              <dt>Recorded</dt><dd><xsl:value-of select="o:date_nonpreferred_format"/></dd>
            </xsl:when>
          </xsl:choose>
          <xsl:if test="o:duration/text()">
            <dt>Duration</dt><dd><xsl:value-of select="o:duration"/></dd>
          </xsl:if>
          <xsl:if test="o:interviewee/text()">
            <dt>Interviewee</dt><dd><xsl:value-of select="o:interviewee"/></dd>
          </xsl:if>
          <xsl:if test="o:interviewer/text()">
            <dt>Interviewer</dt><dd><xsl:value-of select="o:interviewer"/></dd>
          </xsl:if>
          <xsl:if test="o:rights/text()">
            <dt>Copyright</dt><dd><xsl:value-of select="o:rights"/></dd>
          </xsl:if>
          <xsl:if test="o:usage/text()">
            <dt>Conditions of use</dt><dd><xsl:value-of select="o:usage"/></dd>
          </xsl:if>
          <dt>Subject Keywords</dt>
          <dd class="keywords">
            <ul class="keywords">
              <xsl:for-each select="o:subject">
                <li><xsl:value-of select="."></xsl:value-of></li>
              </xsl:for-each>
            </ul>
          </dd>
        </dl>
        <h2>Index</h2>
        <dl class="index">
          <xsl:for-each select="o:index/o:point">
            <dt><xsl:value-of select="floor(o:time div 60)"/>:<xsl:value-of select="format-number(o:time - 60 * floor(o:time div 60), '00')"/></dt>
            <dd>
              <xsl:value-of select="o:title"/>
            </dd>
          </xsl:for-each>
        </dl>
        <h2>Transcript</h2>
        <pre>
          <xsl:value-of select="o:transcript"/>
        </pre>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>
