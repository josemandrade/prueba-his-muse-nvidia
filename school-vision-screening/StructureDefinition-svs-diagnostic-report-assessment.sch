<?xml version="1.0" encoding="UTF-8"?>
<sch:schema xmlns:sch="http://purl.oclc.org/dsdl/schematron" queryBinding="xslt2">
  <sch:ns prefix="f" uri="http://hl7.org/fhir"/>
  <sch:ns prefix="h" uri="http://www.w3.org/1999/xhtml"/>
  <!-- 
    This file contains just the constraints for the profile DiagnosticReport
    It includes the base constraints for the resource as well.
    Because of the way that schematrons and containment work, 
    you may need to use this schematron fragment to build a, 
    single schematron that validates contained resources (if you have any) 
  -->
  <sch:pattern>
    <sch:title>f:DiagnosticReport</sch:title>
    <sch:rule context="f:DiagnosticReport">
      <sch:assert test="count(f:basedOn) &gt;= 1">basedOn: minimum cardinality of 'basedOn' is 1</sch:assert>
      <sch:assert test="count(f:basedOn) &lt;= 1">basedOn: maximum cardinality of 'basedOn' is 1</sch:assert>
      <sch:assert test="count(f:category) &gt;= 1">category: minimum cardinality of 'category' is 1</sch:assert>
      <sch:assert test="count(f:category) &lt;= 1">category: maximum cardinality of 'category' is 1</sch:assert>
      <sch:assert test="count(f:subject) &gt;= 1">subject: minimum cardinality of 'subject' is 1</sch:assert>
      <sch:assert test="count(f:issued) &gt;= 1">issued: minimum cardinality of 'issued' is 1</sch:assert>
      <sch:assert test="count(f:performer) &gt;= 1">performer: minimum cardinality of 'performer' is 1</sch:assert>
      <sch:assert test="count(f:performer) &lt;= 1">performer: maximum cardinality of 'performer' is 1</sch:assert>
      <sch:assert test="count(f:resultsInterpreter) &gt;= 1">resultsInterpreter: minimum cardinality of 'resultsInterpreter' is 1</sch:assert>
      <sch:assert test="count(f:resultsInterpreter) &lt;= 1">resultsInterpreter: maximum cardinality of 'resultsInterpreter' is 1</sch:assert>
      <sch:assert test="count(f:result) &gt;= 1">result: minimum cardinality of 'result' is 1</sch:assert>
    </sch:rule>
  </sch:pattern>
</sch:schema>
