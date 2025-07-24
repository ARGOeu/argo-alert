# Changelog

All notable changes in argo-alert project are documented here

## [v2.0.0](https://github.com/FC4E-CAT/fc4e-cat-ui/releases/tag/v2.0.0) - (2025-07-24)

### Added: 
- ARGO-5020 Add endpoint-type and ui-path-group parameters ([#49](https://github.com/ARGOeu/argo-alert/pull/49))
- ARGO-4247 Handle endpoints belonging to multiple groups - filter by group type ([#48](https://github.com/ARGOeu/argo-alert/pull/48))
- ARGO-4229 Add the ability to skip group contact generation. ([#47](https://github.com/ARGOeu/argo-alert/pull/47))
- ARGO-4216 Generate endpoint notification rules based on group contacts ([#46](https://github.com/ARGOeu/argo-alert/pull/46))


## [v1.0.0](https://github.com/ARGOeu/argo-alert/releases/tag/v.1.0.0) - (2023-02-02)

### Added:
- ARGO-3901 Retrieve contacts from argo-web-api

### Changed:
- ARGO-2856 Update simple feed parameters for json and csv
- ARGO-2856 Update notifications to read contact info from json topology


## [v0.2.1](https://github.com/ARGOeu/argo-alert/releases/tag/V0.2.1) - (2020-12-16)

### Added:
- ARGO-2079 Add original contacts feature when sending to testing emails

### Changed:
- ARGO-2145 Finalize py3 version in argo-alert scripts

### Fixed:
- ARGO-2027 Split gocdb contain email string into individual items


## [v0.2.0](https://github.com/ARGOeu/argo-alert/releases/tag/V0.2.1) - (2019-11-06)

### Added:
- ARGO-2027 Split gocdb contain email string into individual items
- ARGO-1710 publish group item status info
- ARGO-1715 Consolidate alerts for endpoints that belong to multiple endpoint groups
- ARGO-1640 Update alert publisher to forward new event information

### Fixed:
- ARGO-1793 Fix ui_urls in alert mails to point correctly to the new web_ui


## [v0.1.2](https://github.com/ARGOeu/argo-alert/releases/tag/v0.1-2) - (2018-11-09)

### Fixed:
- ARGO-1464 Update requests dep to 2.20


## [v0.1.1](https://github.com/ARGOeu/argo-alert/releases/tag/v0.1-1) - (2018-02-27) 

### Added:
- ARGO-933 Implement argo-alert publisher of argo-streaming events to alerta
- ARGO-931 Alerta-mailer rule generator from gocdb contact data
- ARGO-943 Use requests for verifying cert using capath (directory).
- ARGO 960 Refactor rule generator for using notifications tag
- ARGO-990 Accept a list of kafka endpoints for publisher
- ARGO-999 Add boolean conf parameter for using contact notifications
- ARGO-1026 Support different levels of entity groups when retrieving
- ARGO-996 Add ability to generate rules using a group of test email

### Fixed:
- ARGO-945 Fix endpoint_group field. Lowercase status field values
