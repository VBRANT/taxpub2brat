<?xml version="1.0" encoding="UTF-8" ?>
<!--
Purpose: to extract taxon names from TaxPub documents

David King <djk263@openmail.open.ac.uk>
The Open University, July 2012
For the ViBRANT project, <http://vbrant.eu>
-->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"  xmlns:tp="http://www.plazi.org/taxpub">

	<xsl:output method="text" indent="no" encoding="UTF-8"/>
	<xsl:strip-space elements="*"/>

	<xsl:template match="/">
		<xsl:apply-templates select="//tp:taxon-name">
		</xsl:apply-templates>
	</xsl:template>

	<xsl:template match="tp:taxon-name">
		<xsl:choose>

		<!-- inline mark up of text -->
		<xsl:when test="./text() != ''">
			<xsl:text>taxon-name&#09;</xsl:text>
			<xsl:value-of select="./text()"/>
			<xsl:text>&#10;</xsl:text>
		</xsl:when>

		<!-- in-depth mark up of text -->
		<xsl:otherwise>
			<xsl:for-each select="./tp:taxon-name-part">
				<xsl:value-of select="./@taxon-name-part-type"/>
				<xsl:text>&#09;</xsl:text>
				<xsl:value-of select="./text()"/>
				<xsl:text>&#10;</xsl:text>
			</xsl:for-each>
		</xsl:otherwise>

		</xsl:choose>
	</xsl:template>

</xsl:stylesheet>