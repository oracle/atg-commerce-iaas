# Ansible bcctools modules

---
### Modules

  * [bcc_add_agent - add agent](#bcc_add_agent)
  * [bcc_add_target - add target](#bcc_add_target)
  * [bcc_delete_agent - delete agent](#bcc_delete_agent)
  * [bcc_delete_target - delete target](#bcc_delete_target)
  * [bcc_full_deploy - start a full deployment to a target](#bcc_full_deploy)
  * [bcc_get_agent_id - get an agent id](#bcc_get_agent_id)
  * [bcc_get_target_by_id - get a target by id](#bcc_get_target_by_id)
  * [bcc_get_target_by_name - get a target by name](#bcc_get_target_by_name)
  * [bcc_get_agent_by_id - get an agent by ID](#bcc_get_agent_by_id)
  * [bcc_get_agent_by_name - get an agent by name](#bcc_get_agent_by_name)
  * [bcc_import_topology - import bcc topology](#bcc_import_topology)
  * [bcc_initial_deployment - start the first deployment on a new site](#bcc_initial_deployment)
  * [bcc_initialize_topology - initialize bcc topology](#bcc_initialize_topology)
  * [bcc_is_primary_agent - check if an agent id is a primary agent](#bcc_is_primary_agent)
  * [bcc_is_primary_target - check if a target id is a primary target](#bcc_is_primary_target)
  * [bcc_list_topologies - list all bcc topologies](#bcc_list_topologies)
  * [bcc_login - bcc login](#bcc_login)
  * [bcc_logout - logout a user](#bcc_logout)
  * [bcc_session_confirmation - get a session confirmation number](#bcc_session_confirmation)
  * [bcc_switch_agent_datasource - switch an agents datasource](#bcc_switch_agent_datasource)

---

## <a id="bcc_add_agent"></a> bcc_add_agent
Add agent

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Add an agent to the BCC

#### Options

| Parameter     | required    | default  | choices    | datatype | comments |
| ------------- |-------------| ---------|----------- |--------- |--------- |
| endpoint  |   yes  |  | |  str  |  BCC REST Endpoint  |
| agentDisplayName  |   no  |  | |  str  |  Name of new agent  |
| transportURL  |   yes  |  | |  str  |  Transport URL for the agent  |
| includeAssetDestinations  |   no  |    | |  str  |  Assets to include for this agent. Comma separated values.  |
| targetID  |   yes  |  | |  str  |  Target ID to add this agent to  |
| agentEssential  |   no  |  False  | |  bool  |  Is this an essential agent?  |
| cookie  |   no  |  | |  str  |  ATG Cookie  |
| agentDescription  |   no  |    | |  str  |  Description of new agent  |
| action  |   no  |  add_agent  | <ul> <li>add_agent</li> </ul> |  |  Action to be executed against the BCC  |
| excludeAssetDestinations  |   no  |    | |  str  |  Assets to exclude from this agent. Comma separated values.  |


 
#### Examples

```
- name: Add a new agent
      action: add_agent
      agentDisplayName: "TestAgent"
      agentEssential: True
      transportURL: "rmi://localhost:8001"
      includeAssetDestinations: "/atg/epub/file/ConfigFileSystem,/atg/epub/file/WWWFileSystem"
      targetID: "{{ result.target.targetDef.ID }}"

```



---


## <a id="bcc_add_target"></a> bcc_add_target
Add target

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Add a target to the BCC

#### Options

| Parameter     | required    | default  | choices    | datatype | comments |
| ------------- |-------------| ---------|----------- |--------- |--------- |
| endpoint  |   yes  |  | |  str  |  BCC REST Endpoint  |
| description  |   no  |    | |  str  |  Description of new target  |
| targetName  |   yes  |  | |  str  |  Name of new target  |
| flagAgents  |   no  |  False  | |  bool  |  Flag agents only - do not deploy to target  |
| cookie  |   no  |  | |  str  |  ATG Cookie  |
| delimitedRepositoryMappings  |   no  |    | |  str  |  Mapping for source and destination repositories for this target. Source and destination repositories are separated by $$. Each mapping item is comma separated.  |
| action  |   no  |  add_target  | <ul> <li>add_target</li> </ul> |  |  Action to be executed against the BCC  |
| targetOneOff  |   no  |  False  | |  bool  |  Is this a one off target?  |


 
#### Examples

```
- name: Add a new target
    bcc_add_target:
      action: add_target
      targetName: "Test"
      delimitedRepositoryMappings: "/atg/userprofiling/PersonalizationRepository$$/atg/userprofiling/PersonalizationRepository_production"

```



---


## <a name="bcc_delete_agent"></a> bcc_delete_agent
Delete Agent

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Delete an agent

#### Options

| Parameter     | required    | default  | choices    | datatype | comments |
| ------------- |-------------| ---------|----------- |--------- |--------- |
| action  |   no  |  delete_agent  | <ul> <li>delete_agent</li> </ul> |  |  Action to be executed against the BCC  |
| agentID  |   yes  |  | |  str  |  ID of the agent to delete  |
| cookie  |   no  |  | |  str  |  ATG Cookie  |
| endpoint  |   yes  |  | |  str  |  BCC REST Endpoint  |


 
#### Examples

```

```



---


## <a name="bcc_delete_target"></a> bcc_delete_target
Delete Target

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Delete a target

#### Options

| Parameter     | required    | default  | choices    | datatype | comments |
| ------------- |-------------| ---------|----------- |--------- |--------- |
| action  |   no  |  delete_target  | <ul> <li>delete_target</li> </ul> |  |  Action to be executed against the BCC  |
| cookie  |   no  |  | |  str  |  ATG Cookie  |
| endpoint  |   yes  |  | |  str  |  BCC REST Endpoint  |
| targetID  |   yes  |  | |  str  |  ID of the target to delete  |


 
#### Examples

```

```



---


## <a name="bcc_full_deploy"></a> bcc_full_deploy
Start a full deployment to a target

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Start a full deployment to a target

#### Options

| Parameter     | required    | default  | choices    | datatype | comments |
| ------------- |-------------| ---------|----------- |--------- |--------- |
| action  |   no  |  full_deploy  | <ul> <li>full_deploy</li> </ul> |  |  Action to be executed against the BCC  |
| cookie  |   no  |  | |  str  |  ATG Cookie  |
| endpoint  |   yes  |  | |  str  |  BCC REST Endpoint  |
| targetID  |   yes  |  | |  str  |  ID of the target you want to deploy to  |


 
#### Examples

```

```



---


## <a name="bcc_get_agent_id"></a> bcc_get_agent_id
Get an agent ID

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Get an agent ID based on target name and agent name

#### Options

| Parameter     | required    | default  | choices    | datatype | comments |
| ------------- |-------------| ---------|----------- |--------- |--------- |
| action  |   no  |  get_agent_id  | <ul> <li>get_agent_id</li> </ul> |  |  Action to be executed against the BCC  |
| cookie  |   no  |  | |  str  |  ATG Cookie  |
| endpoint  |   yes  |  | |  str  |  BCC REST Endpoint  |
| targetName  |   yes  |  | |  str  |  Name of the target the agent you want is tied to  |
| agentName  |   yes  |  | |  str  |  Name of the agent you want an ID returned for  |


 
#### Examples

```

```



---


## <a name="bcc_get_target_by_id"></a> bcc_get_target_by_id
Get a target by ID

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Get a target by ID

#### Options

| Parameter     | required    | default  | choices    | datatype | comments |
| ------------- |-------------| ---------|----------- |--------- |--------- |
| action  |   no  |  get_target_by_id  | <ul> <li>get_target_by_id</li> </ul> |  |  Action to be executed against the BCC  |
| cookie  |   no  |  | |  str  |  ATG Cookie  |
| endpoint  |   yes  |  | |  str  |  BCC REST Endpoint  |
| targetID  |   yes  |  | |  str  |  ID of the target you want returned  |


 
#### Examples

```

```



---


## <a name="bcc_get_target_by_name"></a> bcc_get_target_by_name
Get a target by name

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Get a target by name

#### Options

| Parameter     | required    | default  | choices    | datatype | comments |
| ------------- |-------------| ---------|----------- |--------- |--------- |
| action  |   no  |  get_target_by_name  | <ul> <li>get_target_by_name</li> </ul> |  |  Action to be executed against the BCC  |
| cookie  |   no  |  | |  str  |  ATG Cookie  |
| endpoint  |   yes  |  | |  str  |  BCC REST Endpoint  |
| targetName  |   yes  |  | |  str  |  Name of the target you want returned  |


 
#### Examples

```

```



---

## <a name="bcc_get_agent_by_id"></a> bcc_get_agent_by_id
Get an agent by ID

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Get an agent by ID

#### Options

| Parameter     | required    | default  | choices    | datatype | comments |
| ------------- |-------------| ---------|----------- |--------- |--------- |
| action  |   no  |  get_agent_by_id  | <ul> <li>get_agent_by_id</li> </ul> |  |  Action to be executed against the BCC  |
| cookie  |   no  |  | |  str  |  ATG Cookie  |
| endpoint  |   yes  |  | |  str  |  BCC REST Endpoint  |
| agentID  |   yes  |  | |  str  |  ID of the agent you want returned  |


 
#### Examples

```

```


---

## <a name="bcc_get_agent_by_name"></a> bcc_get_agent_by_name
Get an agent by name

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Get an agent by name

#### Options

| Parameter     | required    | default  | choices    | datatype | comments |
| ------------- |-------------| ---------|----------- |--------- |--------- |
| action  |   no  |  get_agent_by_name  | <ul> <li>get_agent_by_name</li> </ul> |  |  Action to be executed against the BCC  |
| cookie  |   no  |  | |  str  |  ATG Cookie  |
| endpoint  |   yes  |  | |  str  |  BCC REST Endpoint  |
| targetName  |   yes  |  | |  str  |  Name of the target the agent is tied to  |
| agentName  |   yes  |  | |  str  |  Name of the agent you want returned  |


 
#### Examples

```

```


---

## <a name="bcc_import_topology"></a> bcc_import_topology
Import BCC topology

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Import BCC topology. Data must be in base64 format, with no line wraps

#### Options

| Parameter     | required    | default  | choices    | datatype | comments |
| ------------- |-------------| ---------|----------- |--------- |--------- |
| action  |   no  |  import  | <ul> <li>import</li> </ul> |  |  Action to be executed against the BCC  |
| endpoint  |   yes  |  | |  str  |  BCC REST Endpoint  |
| cookie  |   no  |  | |  str  |  ATG Cookie  |
| base64XML  |   yes  |  | |  str  |  Topology XML converted to base64, with no line wraps  |


 
#### Examples

```

```



---


## <a name="bcc_initial_deployment"></a> bcc_initial_deployment
Start the first deployment on a new site

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Start the first deployment on a new site

#### Options

| Parameter     | required    | default  | choices    | datatype | comments |
| ------------- |-------------| ---------|----------- |--------- |--------- |
| action  |   no  |  initial_deployment  | <ul> <li>initial_deployment</li> </ul> |  |  Action to be executed against the BCC  |
| cookie  |   no  |  | |  str  |  ATG Cookie  |
| endpoint  |   yes  |  | |  str  |  BCC REST Endpoint  |
| targetID  |   yes  |  | |  str  |  ID of the target you want to deploy to  |
| flagAgents  |   no  |  False  | |  bool  |  Flag agents only - do not do a full deploy  |


 
#### Examples

```

```



---


## <a name="bcc_initialize_topology"></a> bcc_initialize_topology
Initialize BCC topology

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Initialize BCC topology. This makes any pending changes live.

#### Options

| Parameter     | required    | default  | choices    | datatype | comments |
| ------------- |-------------| ---------|----------- |--------- |--------- |
| action  |   no  |  initialize  | <ul> <li>initialize</li> </ul> |  |  Action to be executed against the BCC  |
| cookie  |   no  |  | |  str  |  ATG Cookie  |
| endpoint  |   yes  |  | |  str  |  BCC REST Endpoint  |
| targetID  |   no  |    | |  str  |  Comma separated list of target ID's. This is optional. If passed in, the target ID's listed will be flagged only. No deploy will occur.  |


 
#### Examples

```

```



---


## <a name="bcc_is_primary_agent"></a> bcc_is_primary_agent
Check if an agent ID is a primary agent

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Check if an agent ID is a primary agent

#### Options

| Parameter     | required    | default  | choices    | datatype | comments |
| ------------- |-------------| ---------|----------- |--------- |--------- |
| action  |   no  |  is_primary_agent  | <ul> <li>is_primary_agent</li> </ul> |  |  Action to be executed against the BCC  |
| agentID  |   yes  |  | |  str  |  ID of the agent you want to check  |
| cookie  |   no  |  | |  str  |  ATG Cookie  |
| endpoint  |   yes  |  | |  str  |  BCC REST Endpoint  |


 
#### Examples

```

```



---


## <a name="bcc_is_primary_target"></a> bcc_is_primary_target
Check if a target ID is a primary target

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Check if a target ID is a primary target

#### Options

| Parameter     | required    | default  | choices    | datatype | comments |
| ------------- |-------------| ---------|----------- |--------- |--------- |
| action  |   no  |  is_primary_target  | <ul> <li>is_primary_target</li> </ul> |  |  Action to be executed against the BCC  |
| cookie  |   no  |  | |  str  |  ATG Cookie  |
| endpoint  |   yes  |  | |  str  |  BCC REST Endpoint  |
| targetID  |   yes  |  | |  str  |  ID of the target you want to check  |


 
#### Examples

```

```



---


## <a name="bcc_list_topologies"></a> bcc_list_topologies
List all BCC topologies

  * Synopsis
  * Options
  * Examples

#### Synopsis
 List all BCC topologies

#### Options

| Parameter     | required    | default  | choices    | datatype | comments |
| ------------- |-------------| ---------|----------- |--------- |--------- |
| action  |   no  |  list  | <ul> <li>list</li> </ul> |  |  Action to be executed against the BCC  |
| endpoint  |   yes  |  | |  str  |  BCC REST Endpoint  |
| cookie  |   no  |  | |  str  |  ATG Cookie  |


 
#### Examples

```

```



---


## <a name="bcc_login"></a> bcc_login
BCC Login

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Log a user in to the BCC/CA instance

#### Options

| Parameter     | required    | default  | choices    | datatype | comments |
| ------------- |-------------| ---------|----------- |--------- |--------- |
| action  |   no  |  login  | <ul> <li>login</li> </ul> |  |  Action to be executed against the BCC  |
| username  |   yes  |  | |  str  |  Username to login with  |
| password  |   yes  |  | |  str  |  Password of the user to login with  |
| endpoint  |   yes  |  | |  str  |  BCC REST Endpoint  |
| cookie  |   no  |  | |  str  |  ATG Cookie  |


 
#### Examples

```

```



---


## <a name="bcc_logout"></a> bcc_logout
Logout a user

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Logout a user

#### Options

| Parameter     | required    | default  | choices    | datatype | comments |
| ------------- |-------------| ---------|----------- |--------- |--------- |
| action  |   no  |  logout  | <ul> <li>logout</li> </ul> |  |  Action to be executed against the BCC  |
| endpoint  |   yes  |  | |  str  |  BCC REST Endpoint  |
| cookie  |   no  |  | |  str  |  ATG Cookie.  |


 
#### Examples

```

```



---


## <a name="bcc_session_confirmation"></a> bcc_session_confirmation
Get a session confirmation number

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Get a session confirmation number (_dynSessConf)

#### Options

| Parameter     | required    | default  | choices    | datatype | comments |
| ------------- |-------------| ---------|----------- |--------- |--------- |
| action  |   no  |  get_session  | <ul> <li>get_session</li> </ul> |  |  Action to be executed against the BCC  |
| endpoint  |   yes  |  | |  str  |  BCC REST Endpoint  |


 
#### Examples

```

```



---


## <a name="bcc_switch_agent_datasource"></a> bcc_switch_agent_datasource
Switch an agents datasource

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Switch an agents datasource

#### Options

| Parameter     | required    | default  | choices    | datatype | comments |
| ------------- |-------------| ---------|----------- |--------- |--------- |
| action  |   no  |  switch_agent_datasource  | <ul> <li>switch_agent_datasource</li> </ul> |  |  Action to be executed against the BCC  |
| endpoint  |   yes  |  | |  str  |  BCC REST Endpoint  |
| cookie  |   no  |  | |  str  |  ATG Cookie  |
| switchTargetID  |   yes  |  | |  str  |  ID of the target the agent(s) you want to switch belong to  |
| agentIDs  |   yes  |  | |  str  |  ID's of the agents you want to switch datasources on  Comma separated list of ID's  |


 
#### Examples

```

```



---


---
Oracle A-Team

