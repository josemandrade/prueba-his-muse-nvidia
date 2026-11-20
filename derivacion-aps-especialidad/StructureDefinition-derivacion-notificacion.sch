<?xml version="1.0" encoding="UTF-8"?>
<sch:schema xmlns:sch="http://purl.oclc.org/dsdl/schematron" queryBinding="xslt2">
  <sch:ns prefix="f" uri="http://hl7.org/fhir"/>
  <sch:ns prefix="h" uri="http://www.w3.org/1999/xhtml"/>
  <!-- 
    This file contains just the constraints for the profile Communication
    It includes the base constraints for the resource as well.
    Because of the way that schematrons and containment work, 
    you may need to use this schematron fragment to build a, 
    single schematron that validates contained resources (if you have any) 
  -->
  <sch:pattern>
    <sch:title>f:Communication</sch:title>
    <sch:rule context="f:Communication">
      <sch:assert test="count(f:extension[@url = 'https://josemandrade.github.io/prueba-his-muse-nvidia/StructureDefinition/derivacion-delivery-outcome']) &lt;= 1">extension with URL = 'https://josemandrade.github.io/prueba-his-muse-nvidia/StructureDefinition/derivacion-delivery-outcome': maximum cardinality of 'extension' is 1</sch:assert>
      <sch:assert test="count(f:identifier) &gt;= 1">identifier: minimum cardinality of 'identifier' is 1</sch:assert>
      <sch:assert test="count(f:basedOn) &gt;= 1">basedOn: minimum cardinality of 'basedOn' is 1</sch:assert>
      <sch:assert test="count(f:medium) &gt;= 1">medium: minimum cardinality of 'medium' is 1</sch:assert>
      <sch:assert test="count(f:subject) &gt;= 1">subject: minimum cardinality of 'subject' is 1</sch:assert>
      <sch:assert test="count(f:sent) &gt;= 1">sent: minimum cardinality of 'sent' is 1</sch:assert>
      <sch:assert test="count(f:recipient) &gt;= 1">recipient: minimum cardinality of 'recipient' is 1</sch:assert>
      <sch:assert test="count(f:sender) &gt;= 1">sender: minimum cardinality of 'sender' is 1</sch:assert>
    </sch:rule>
  </sch:pattern>
</sch:schema>
