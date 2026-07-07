# Usuale Ontology and TEI Integration

## Purpose

Usuale uses TEI XML to encode concrete liturgical texts and their textual
structure. A separate RDF/OWL ontology should define the shared semantic
vocabulary for liturgical text types, text parts, and relationships.

The two layers have different responsibilities:

- **TEI** records text, structure, witnesses, variants, bibliography, notation
  links, and editorial metadata.
- **OWL** defines classes and properties such as `LiturgicalText`,
  `Antiphon`, `Responsory`, `Incipit`, `hasPart`, and `sungWith`.
- **TEI ODD, Relax NG, and Schematron** validate the permitted XML structure.
- **SHACL**, if later introduced, may validate RDF data exported from TEI.

OWL is not an XML schema and must not replace TEI validation.

## Repository Location

The editable ontology should live in the repository:

```text
ontology/
├── usuale-liturgical-texts.ttl
├── README.md
└── generated/
    └── usuale-liturgical-texts.rdf
```

Turtle is the preferred authoritative serialization because it is compact and
Git-friendly. RDF/XML or JSON-LD may be generated for applications that need
them. Generated serializations should not be edited independently.

## Ontology Scope

The first ontology module should remain deliberately small. It should describe
liturgical text types and their parts before attempting to model the complete
calendar, rubrical system, or theology of the liturgy.

An initial class hierarchy may include:

```text
LiturgicalText
├── Chant
│   ├── Antiphon
│   │   └── PsalmAntiphon
│   ├── Responsory
│   │   ├── GreatResponsory
│   │   └── ShortResponsory
│   ├── Hymn
│   ├── Introit
│   ├── Gradual
│   ├── Alleluia
│   ├── Tract
│   ├── Offertory
│   └── Communion
├── Reading
│   ├── Epistle
│   ├── Gospel
│   └── PatristicReading
├── Oration
│   ├── Collect
│   ├── Secret
│   └── Postcommunion
├── Psalm
└── Canticle

LiturgicalTextPart
├── Incipit
├── Continuation
├── LiturgicalAsterisk
├── Response
├── ResponsoryVerse
├── Repetition
└── Doxology
```

This hierarchy is provisional. A class should be introduced only when it has a
clear definition and at least one expected use in Usuale data.

Possible object properties include:

```text
hasPart
isPartOf
hasTextWitness
hasUsage
usedIn
sungWith
hasNotation
hasSource
```

Property domains, ranges, inverses, and cardinality restrictions should be
added cautiously. OWL uses an open-world model: missing information is not
automatically false.

## Classes and TEI Resources

Ontology terms such as `Antiphon` are OWL classes. A concrete TEI resource,
for example the `div` containing *Ecce sacerdos magnus*, represents an
individual instance of such a class.

Conceptually, this TEI fragment:

```xml
<div xml:id="ant-ecce-sacerdos-magnus.text"
     type="antiphon"
     ana="ONTOLOGY_BASE_IRI#PsalmAntiphon">
```

corresponds to an RDF statement such as:

```turtle
<ANTIPHON_DOCUMENT_IRI#ant-ecce-sacerdos-magnus.text>
    a lit:PsalmAntiphon .
```

The exact document IRI used in exported RDF requires a separate URI policy for
TEI resources. It must not be inferred from a local filesystem path.

## Use of TEI Attributes

Use `@type` and `@ana` together:

```xml
<div type="antiphon"
     ana="ONTOLOGY_BASE_IRI#Antiphon">
```

- `@type` is the compact local TEI classification used by XML processing,
  ODD, Relax NG, Schematron, XPath, and XSLT.
- `@ana` links the encoded resource to one or more externally defined semantic
  interpretations.

TEI P5 defines `@ana` as one or more whitespace-separated pointers. It may
therefore carry more than one compatible class IRI:

```xml
<div type="antiphon"
     ana="ONTOLOGY_BASE_IRI#Antiphon
          ONTOLOGY_BASE_IRI#PsalmAntiphon">
```

Text parts may be classified in the same way:

```xml
<seg type="incipit"
     ana="ONTOLOGY_BASE_IRI#Incipit">Ecce sacérdos magnus</seg>

<caesura type="asteriscus"
         ana="ONTOLOGY_BASE_IRI#LiturgicalAsterisk"/>

<seg type="continuatio"
     ana="ONTOLOGY_BASE_IRI#Continuation">qui in diébus suis ...</seg>
```

Until the permanent ontology namespace has been reserved, production TEI files
must not use speculative `w3id.org` IRIs. `ONTOLOGY_BASE_IRI` in this document
is a placeholder, not an assigned identifier.

## Persistent Namespace

The preferred public namespace pattern is:

```text
https://w3id.org/usuale/ontology#
```

Example class IRI:

```text
https://w3id.org/usuale/ontology#Antiphon
```

This namespace is only a proposal until it has been accepted by the
`w3id.org` maintainers. Availability must be checked and the identifier must be
registered before it is written into project data.

The ontology should declare:

```turtle
@prefix owl: <http://www.w3.org/2002/07/owl#> .

<https://w3id.org/usuale/ontology>
    a owl:Ontology ;
    owl:versionIRI <https://w3id.org/usuale/ontology/0.1.0> .
```

The unversioned ontology IRI and class IRIs remain stable. `owl:versionIRI`
identifies a specific released version.

## Hosting Architecture

Persistent identification, current delivery, and archival preservation are
separate concerns:

```text
TEI @ana / RDF data
        |
        v
https://w3id.org/usuale/ontology#Antiphon
        |
        v
redirect or content negotiation
        |
        v
current ontology on institutional hosting or GitHub Pages
        |
        +--> release snapshots archived in Zenodo
```

### w3id.org

`w3id.org` is the preferred persistent namespace provider. It is an HTTPS
redirection service operated by the W3C Permanent Identifier Community Group.
Redirect rules are managed through pull requests to:

```text
https://github.com/perma-id/w3id.org
```

It does not replace ontology hosting. It gives Usuale a stable public IRI whose
current destination can be changed later.

For a hash namespace, requests for individual classes such as
`#Antiphon` retrieve the ontology document itself; the fragment is interpreted
client-side. This is simple and suitable for a small ontology.

### Registering the w3id.org namespace

There is no separate registration form. A namespace is requested by adding its
redirect configuration to the `perma-id/w3id.org` repository and submitting a
pull request.

The proposed registration procedure is:

1. Fork <https://github.com/perma-id/w3id.org>.
2. Create a top-level directory named `usuale`.
3. Add at least:

   ```text
   usuale/
   ├── .htaccess
   └── README.md
   ```

4. In `README.md`, describe the namespace, its destination, and the responsible
   maintainer or maintainers. Include durable contact information, normally
   GitHub usernames and optionally email addresses.
5. In `.htaccess`, define the redirects from `w3id.org` to the current ontology
   host. The rules may also implement HTTP content negotiation for HTML,
   Turtle, RDF/XML, or JSON-LD.
6. Commit the directory on a branch in the fork and open a pull request against
   the `master` branch of `perma-id/w3id.org`.
7. Respond to review requests from the w3id.org maintainers. The namespace is
   reserved only after the pull request has been accepted and merged.
8. Test both the ontology document IRI and the desired representations after
   the merge.

An illustrative `.htaccess` configuration is:

```apache
RewriteEngine On

RewriteCond %{HTTP_ACCEPT} text/turtle
RewriteRule ^ontology/?$ ONTOLOGY_TURTLE_URL [R=303,L]

RewriteCond %{HTTP_ACCEPT} application/rdf\+xml
RewriteRule ^ontology/?$ ONTOLOGY_RDF_XML_URL [R=303,L]

RewriteRule ^ontology/?$ ONTOLOGY_HTML_URL [R=303,L]
```

The three destination values are placeholders. They must be replaced with
publicly reachable URLs before the pull request is submitted. Redirect status
`303 See Other` is suitable when the ontology IRI identifies the ontology as a
semantic resource and the target is one of its document representations.

Because `https://w3id.org/usuale/ontology#Antiphon` uses a fragment identifier,
the browser or RDF client requests only
`https://w3id.org/usuale/ontology`; `#Antiphon` is not sent to the server.
Consequently, the server rule redirects the ontology document, not each class
separately.

If submitting a pull request is not possible, the repository documentation
also gives `public-perma-id@w3.org` as a contact route. A pull request is
preferable because it makes the requested rules, maintainers, and review
history public and version-controlled.

The proposed `usuale` path appeared unassigned when checked on 23 June 2026:
`https://w3id.org/usuale/` returned HTTP 404, and no corresponding directory
was present in the current `perma-id/w3id.org` repository tree. This was only
an availability check, not a reservation. Until the registration pull request
has been merged, Usuale must continue to treat the namespace as provisional
and must not use it in production TEI `@ana` values.

### Current ontology hosting

The redirect target may initially be:

- institutional web hosting, if long-term support is available; or
- GitHub Pages generated from the ontology directory.

Institutional hosting is preferable when a durable institutional commitment
exists. GitHub Pages is a practical initial deployment target because the
ontology remains version-controlled and publication can be automated.

The server should provide at least Turtle and preferably RDF/XML or JSON-LD.
Content negotiation may return different serializations for the ontology
document, while a human-readable HTML description may be offered to browsers.

### Zenodo

Each significant ontology release should additionally be archived in Zenodo.
Zenodo supplies a DOI and an immutable, citable release snapshot.

The DOI is used for citation and preservation. It should not replace class IRIs:

- class identity: `https://w3id.org/usuale/ontology#Antiphon`
- ontology version: `owl:versionIRI`
- archived release citation: Zenodo DOI

## Versioning Policy

Published class and property IRIs must be treated as permanent.

- Do not change the meaning of an existing term incompatibly.
- Prefer deprecation with `owl:deprecated true` over deletion.
- Introduce a new IRI when a concept changes identity.
- Keep labels and definitions multilingual where useful.
- Record release history with `owl:versionInfo`, `dcterms:issued`, and
  `dcterms:modified`.
- Archive released ontology files and release notes.

The ontology may evolve before its first public release, but once TEI data or
external projects use a public class IRI, renaming it becomes a migration.

## Validation and Synchronization

The project should eventually validate three layers:

1. **TEI structure**: ODD-generated Relax NG and Schematron.
2. **Ontology syntax and consistency**: RDF parser and OWL reasoner.
3. **TEI-to-ontology links**: every IRI in relevant `@ana` attributes resolves
   to a declared ontology class or property.

The ODD may constrain local `@type` values and Schematron may verify their
mapping to expected ontology IRIs. For example, a `div[@type='antiphon']`
should carry an `@ana` value identifying `Antiphon` or one of its subclasses.

OWL should describe semantic relationships; it should not be used to require
the presence or order of TEI elements.

## Implementation Sequence

1. Draft the minimal ontology locally in Turtle.
2. Define the first classes and natural-language definitions.
3. Decide the mapping from existing TEI `@type` values to OWL classes.
4. Add tests for RDF syntax and TEI `@ana` targets.
5. Select the current hosting target.
6. Confirm and register the permanent `w3id.org` namespace.
7. Replace `ONTOLOGY_BASE_IRI` placeholders in documentation and add real
   `@ana` links to TEI data.
8. Publish the first version and archive it in Zenodo.

## References

- TEI P5 `att.global.analytic` and `@ana`:
  <https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-att.global.analytic.html>
- OWL 2 Primer:
  <https://www.w3.org/TR/owl2-primer/>
- RDF 1.1 Concepts:
  <https://www.w3.org/TR/rdf11-concepts/>
- Permanent Identifiers for the Web:
  <https://w3id.org/>
- w3id.org repository and registration process:
  <https://github.com/perma-id/w3id.org>
- Zenodo:
  <https://zenodo.org/>
