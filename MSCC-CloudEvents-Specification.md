
# MSCC CloudEvents Naming Convention
- Author: Abhaykumar Raut <abhaykumar.raut@atos.net>




This document provides deatails of naming convention for cloud event 
| Element | Description     | MSCC naming convention | Example for K8S Event Exporter |
| :-------- | :------- | :------------------------- | :------------------------- |
| id | A unique identifier for the event | <unique id> | a931b41a-76bf-4573-bdf7-8a85b3068f6b |
| source | The source of the event, usually a URL or URI | mscc://<tenant>/<instance in tenant>/<component> | mscc://core/0/control-plane, mscc://acme/0/control-plane |
| type | The type of the event, which categorizes it | <reverse domain>.<atos event type> | net.atos.mscc.composition-ready |

Below table provides the details of placolders  mentioned in the MSCC naming convetion from ablove table 
| Parameter | Naming Convention     | Description | Example/Comments |
| :-------- | :------- |  ------------------------- | :------------------------- |
| <tenant> | core | Atos Core tenant | core |
|  | tenant  | Customer tenant | acme |
| <instance in tenant> | for now number: 0,1,… | instance in tenant - number for now | net.atos.mscc.composition-ready |
| <component> | control-plane | Hardcoded value for core - for now | control-plane |
| <reverse domain> | net.atos.mscc | Atos domain name in reverse notation | net.atos.mscc.composition-ready |
| <unique id> | <8 signs>-<4 signs>-<4 signs>-<12 signs>  |	a931b41a-76bf-4573-bdf7-8a85b3068f6b | Taken from K8S Event ID




## Note
Other information will be kept inside data field