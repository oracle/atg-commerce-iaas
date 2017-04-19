# API documentation for BCCTools REST services

Note that the complete URL must follow the ATG MVC REST framework format.  
For example, the URL to get a session confirmation number is /atg/rest/SessionConfirmationActor. That must be prefixed with /rest/model.

### API's
  * [Add Target](#addTarget)
  * [Update Target](#updateTarget)
  * [Delete Target](#deleteTarget)
  * [Add Agent](#addAgent)
  * [Update Agent](#updateAgent)
  * [Delete Agent](#deleteAgent)  
  * [Initialize Topology](#initializeTopology)  
  * [Get All Topologies](#getAllTopologies)
  * [Get Target By ID](#getTargetByID)
  * [Is Primary Target](#isPrimaryTarget)
  * [Is Primary Agent](#isPrimaryAgent)
  * [Get Target By Name](#getTargetByName)
  * [Get Live Target By Name](#getLiveTargetByName)
  * [Full Deployment](#fullDeployNow)
  * [Switch Agent Datasources](#switchAgentDatastores)
  * [Get Agent ID from name](#getAgentID)
  * [Import topology from XML](#importFromXML)
  * [Get a session confirmation number](#getSessionConfirmationNumber)
  * [Log a user in](#loginUser)    
  * [Log a user out](#logoutUser)

**Add Target** <a id="addTarget">
----
  Add a target

* **URL**

  /com/oracle/ateam/bcctools/BCCActor/addTarget

* **Method:**

  `POST`
  
*  **Data Params**

   **Required:**
 
   `targetDisplayName=[string]` display name for the target
   
   **Optional:**
   
   `description=[string]` description of the target <br />
   `flagAgents=[boolean]` flag agents only(do not do a deploy) <br />
   `targetOneOff=[boolean]` Is this a one-off target <br />
   `delimitedRepositoryMappings=[string]` Mapping for source and destination repositories for this target. Source and destination repositories are separated by $$. Each mapping item is comma separated.


* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{}`
 
* **Error Response:**

  * **Code:** 409 <br />
    **Content:** `Your session expired due to inactivity`

  OR

  * **Code:** 200 <br />
    **Content:** `{"error":{"localizedMessage":"User must be logged in to access this resource","messageCode":"USER_NOT_AUTHENTICATED"}}`

* **Sample Call:**

  ```
  curl -L -v -b cookies.txt -H "Content-Type: application/json" -d \"{"targetName\":\"TestTarget\", \"targetDescription\":\"Test\", \"delimitedRepositoryMappings\":\"/atg/userprofiling/PersonalizationRepository\$\$/atg/userprofiling/PersonalizationRepository_production\"}" "http://localhost:7103/rest/model/com/oracle/ateam/bcctools/BCCActor/addTarget"
  ```
  
**Update Target** <a id="updateTarget">
----
  Update a target

* **URL**

  /com/oracle/ateam/bcctools/BCCActor/updateTarget

* **Method:**

  `POST`
  
*  **Data Params**

   **Required:**
 
   `targetID=[string]` ID of the target to update
   
   **Optional:**
   
   `description=[string]` description of the target <br />
   `targetDisplayName=[string]` display name for the target <br />
   `flagAgents=[boolean]` flag agents only(do not do a deploy) <br />
   `targetOneOff=[boolean]` Is this a one-off target <br />
   `delimitedRepositoryMappings=[string]` Mapping for source and destination repositories for this target. Source and destination repositories are separated by $$. Each mapping item is comma separated.


* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{}`
 
* **Error Response:**

  * **Code:** 409 <br />
    **Content:** `Your session expired due to inactivity`

  OR

  * **Code:** 200 <br />
    **Content:** `{"error":{"localizedMessage":"User must be logged in to access this resource","messageCode":"USER_NOT_AUTHENTICATED"}}`

**Delete Target** <a id="deleteTarget">
----
  Delete a target

* **URL**

  /com/oracle/ateam/bcctools/BCCActor/deleteTarget

* **Method:**

  `POST`
  
*  **Data Params**

   **Required:**
 
   `targetID=[string]` ID of the target to delete
   
* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{}`
 
* **Error Response:**

  * **Code:** 409 <br />
    **Content:** `Your session expired due to inactivity`

  OR

  * **Code:** 200 <br />
    **Content:** `{"error":{"localizedMessage":"User must be logged in to access this resource","messageCode":"USER_NOT_AUTHENTICATED"}}`


**Add Agent** <a id="addAgent">
----
  Add an agent

* **URL**

  /com/oracle/ateam/bcctools/BCCActor/addAgent

* **Method:**

  `POST`
  
*  **Data Params**

   **Required:**
 
   `agentDisplayName=[string]` display name for the agent
   
   **Optional:**
   
   `description=[string]` description of the agent <br />
   `excludeAssetDestinations=[string array]` Assets to exclude for this agent. Array of comma separated values. <br />
   `includeAssetDestinations=[string array]` Assets to include for this agent. Array of comma separated values. <br />
   `agentEssential=[boolean]` is this agent essential <br />
   `transportURL=[string]` transport URL for agent <br />
   `targetID=[string]` targetID this agent is associated to <br />


* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{}`
 
* **Error Response:**

  * **Code:** 409 <br />
    **Content:** `Your session expired due to inactivity`

  OR

  * **Code:** 200 <br />
    **Content:** `{"error":{"localizedMessage":"User must be logged in to access this resource","messageCode":"USER_NOT_AUTHENTICATED"}}`

* **Sample Call:**

  ``` 
  curl -L -v -b cookies.txt -H "Content-Type: application/json" -d "{\"targetID\":\"tar80\", \"agentDisplayName\":\"TestAgent\", \"transportURL\":\"rmi://localhost:1235/atg/epub/AgentTransport\", \"includeAssetDestinations\":[\"/atg/epub/file/ConfigFileSystem\",\"/atg/epub/file/WWWFileSystem\"]}" "http://localhost:7103/rest/model/com/oracle/ateam/bcctools/BCCActor/addAgent"
  ```
  
**Update Agent** <a id="updateAgent">
----
  Update an agent

* **URL**

  /com/oracle/ateam/bcctools/BCCActor/updateAgent

* **Method:**

  `POST`
  
*  **Data Params**

   **Required:**
 
   `agentID=[string]` agentID to update <br />
   `targetID=[string]` targetID this agent is associated to <br />   
   
   **Optional:**
   `agentDisplayName=[string]` display name for the agent <br />
   `description=[string]` description of the agent <br />
   `excludeAssetDestinations=[string array]` Assets to exclude for this agent. Array of comma separated values. <br />
   `includeAssetDestinations=[string array]` Assets to include for this agent. Array of comma separated values. <br />
   `agentEssential=[boolean]` is this agent essential <br />
   `transportURL=[string]` transport URL for agent <br />



* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{}`
 
* **Error Response:**

  * **Code:** 409 <br />
    **Content:** `Your session expired due to inactivity`

  OR

  * **Code:** 200 <br />
    **Content:** `{"error":{"localizedMessage":"User must be logged in to access this resource","messageCode":"USER_NOT_AUTHENTICATED"}}`

**Delete Agent** <a id="deleteAgent">
----
  Delete an agent

* **URL**

  /com/oracle/ateam/bcctools/BCCActor/deleteAgent

* **Method:**

  `POST`
  
*  **Data Params**

   **Required:**
 
   `agentID=[string]` agentID to delete <br />
   
   **Optional:**
    None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{}`
 
* **Error Response:**

  * **Code:** 409 <br />
    **Content:** `Your session expired due to inactivity`

  OR

  * **Code:** 200 <br />
    **Content:** `{"error":{"localizedMessage":"User must be logged in to access this resource","messageCode":"USER_NOT_AUTHENTICATED"}}`

**Initialize Topology** <a id="initializeTopology">
----
  Initialize Topology. Required after make any changes to a topology (add, update or delete). This makes changes live.

* **URL**

  /com/oracle/ateam/bcctools/BCCActor/initializeTopology

* **Method:**

  `POST`
  
*  **Data Params**

   **Required:**
    None
   
   **Optional:**
    `surrogateTargetIDToInitOptionMap=[string]` Comma separated list of target ID's. This is optional. If passed in, the target ID's listed will be flagged only. No deploy will occur. <br />

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{}`
 
* **Error Response:**

  * **Code:** 409 <br />
    **Content:** `Your session expired due to inactivity`

  OR

  * **Code:** 200 <br />
    **Content:** `{"error":{"localizedMessage":"User must be logged in to access this resource","messageCode":"USER_NOT_AUTHENTICATED"}}`

**Get All Topologies** <a id="getAllTopologies">
----
  Get all defined topologies 

* **URL**

  /com/oracle/ateam/bcctools/BCCActor/getAllTopologies

* **Method:**

  `POST`
  
*  **Data Params**

   **Required:**
    None
   
   **Optional:**
    None
    
* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{"topologies":[{"ID":"200001",.........}`
 
* **Error Response:**

  * **Code:** 409 <br />
    **Content:** `Your session expired due to inactivity`

  OR

  * **Code:** 200 <br />
    **Content:** `{"error":{"localizedMessage":"User must be logged in to access this resource","messageCode":"USER_NOT_AUTHENTICATED"}}`

**Get Target By ID** <a id="getTargetByID">
----
  Get a target by its ID

* **URL**

  /com/oracle/ateam/bcctools/BCCActor/getTargetByID

* **Method:**

  `POST`
  
*  **Data Params**

   **Required:**
    `targetID=[string]` targetID to get <br />
   
   **Optional:**
    None
    
* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{"target":{"ID":"tar334","agents":[{"ID":"2800005",.........}`
 
* **Error Response:**

  * **Code:** 409 <br />
    **Content:** `Your session expired due to inactivity`

  OR

  * **Code:** 200 <br />
    **Content:** `{"error":{"localizedMessage":"User must be logged in to access this resource","messageCode":"USER_NOT_AUTHENTICATED"}}`


**Is Primary Target** <a id="isPrimaryTarget">
----
  Check if a target is a primary target

* **URL**

  /com/oracle/ateam/bcctools/BCCActor/isPrimaryTarget

* **Method:**

  `POST`
  
*  **Data Params**

   **Required:**
    `targetID=[string]` targetID to check <br />
   
   **Optional:**
    None
    
* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{"isPrimary":true}` `{"isPrimary":false}`
 
* **Error Response:**

  * **Code:** 409 <br />
    **Content:** `Your session expired due to inactivity`

  OR

  * **Code:** 200 <br />
    **Content:** `{"error":{"localizedMessage":"User must be logged in to access this resource","messageCode":"USER_NOT_AUTHENTICATED"}}`

**Is Primary Agent** <a id="isPrimaryAgent">
----
  Check if an agent is a primary agent

* **URL**

  /com/oracle/ateam/bcctools/BCCActor/isPrimaryAgent

* **Method:**

  `POST`
  
*  **Data Params**

   **Required:**
    `agentID=[string]` agentID to check <br />
   
   **Optional:**
    None
    
* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{"isPrimary":true}` `{"isPrimary":false}`
 
* **Error Response:**

  * **Code:** 409 <br />
    **Content:** `Your session expired due to inactivity`

  OR

  * **Code:** 200 <br />
    **Content:** `{"error":{"localizedMessage":"User must be logged in to access this resource","messageCode":"USER_NOT_AUTHENTICATED"}}`

**Get Target By Name** <a id="getTargetByName">
----
  Get a target by its name, and return its targetDef. This checks surrogate/editable targets.

* **URL**

  /com/oracle/ateam/bcctools/BCCActor/getTargetByName

* **Method:**

  `POST`
  
*  **Data Params**

   **Required:**
    `targetName=[string]` target name to get <br />
   
   **Optional:**
    None
    
* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{"targetDef":{"ID":"tar341","agents":[{"ID":"2900002",`
 
* **Error Response:**

  * **Code:** 409 <br />
    **Content:** `Your session expired due to inactivity`

  OR

  * **Code:** 200 <br />
    **Content:** `{"error":{"localizedMessage":"User must be logged in to access this resource","messageCode":"USER_NOT_AUTHENTICATED"}}`

**Get Live Target By Name** <a id="getLiveTargetByName">
----
  Get a live target by its name, and return its targetDef. This checks live targets - these are not directly editable.

* **URL**

  /com/oracle/ateam/bcctools/BCCActor/getLiveTargetByName

* **Method:**

  `POST`
  
*  **Data Params**

   **Required:**
    `targetName=[string]` target name to get <br />
   
   **Optional:**
    None
    
* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{"targetDef":{"ID":"tar341","agents":[{"ID":"2900002",`
 
* **Error Response:**

  * **Code:** 409 <br />
    **Content:** `Your session expired due to inactivity`

  OR

  * **Code:** 200 <br />
    **Content:** `{"error":{"localizedMessage":"User must be logged in to access this resource","messageCode":"USER_NOT_AUTHENTICATED"}}`

**Full Deployment** <a id="fullDeployNow">
----
  Start a full deploy now.

* **URL**

  /com/oracle/ateam/bcctools/BCCActor/fullDeployNow

* **Method:**

  `POST`
  
*  **Data Params**

   **Required:**
    `fullDeployTarget=[string]` ID of the target site you want to deploy <br />
   
   **Optional:**
    None
    
* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{}`
 
* **Error Response:**

  * **Code:** 409 <br />
    **Content:** `Your session expired due to inactivity`

  OR

  * **Code:** 200 <br />
    **Content:** `{"error":{"localizedMessage":"User must be logged in to access this resource","messageCode":"USER_NOT_AUTHENTICATED"}}`

**Switch Agent Datasources** <a id="switchAgentDatastores">
----
  Switch the datasource on specified agents.

* **URL**

  /com/oracle/ateam/bcctools/BCCActor/switchAgentDatastores

* **Method:**

  `POST`
  
*  **Data Params**

   **Required:**
    `agentIDs=[string]` Comma seperated list of agentID's you want to perform the switch on <br />
    `switchTargetID=[string]` The target ID of the target the agents belong to <br />
   
   **Optional:**
    None
    
* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{}`
 
* **Error Response:**

  * **Code:** 409 <br />
    **Content:** `Your session expired due to inactivity`

  OR

  * **Code:** 200 <br />
    **Content:** `{"error":{"localizedMessage":"User must be logged in to access this resource","messageCode":"USER_NOT_AUTHENTICATED"}}`
    
**Get Agent ID by name** <a id="getAgentID">
----
  Get the ID of an agent from its name.

* **URL**

  /com/oracle/ateam/bcctools/BCCActor/getAgentID

* **Method:**

  `POST`
  
*  **Data Params**

   **Required:**
    `targetName=[string]` target name the agent belongs to <br />
    `agentName=[string]` name of the agent you want to get <br />
   
   **Optional:**
    None
    
* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{"agentId":"2900002"}`
 
* **Error Response:**

  * **Code:** 409 <br />
    **Content:** `Your session expired due to inactivity`

  OR

  * **Code:** 200 <br />
    **Content:** `{"error":{"localizedMessage":"User must be logged in to access this resource","messageCode":"USER_NOT_AUTHENTICATED"}}`
    
**Import existing topology XML** <a id="importFromXML">
----
  Import an existing topology xml definition

* **URL**

  /com/oracle/ateam/bcctools/BCCActor/importFromXML

* **Method:**

  `POST`
  
*  **Data Params**

   **Required:**
    `xmlData=[string]` base64 encoded topology definition. This should be one continuous string, no line wraps. <br />
   
   **Optional:**
    None
    
* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{"imported":"true"}` `{"imported":"false"}`
 
* **Error Response:**

  * **Code:** 409 <br />
    **Content:** `Your session expired due to inactivity`

  OR

  * **Code:** 200 <br />
    **Content:** `{"error":{"localizedMessage":"User must be logged in to access this resource","messageCode":"USER_NOT_AUTHENTICATED"}}`
    
**Get a session confirmation number** <a id="getSessionConfirmationNumber">
----
  Get a session confirmation number (_dynSessConf)

* **URL**

  /atg/rest/SessionConfirmationActor/getSessionConfirmationNumber

* **Method:**

  `GET`
  
*  **Data Params**

   **Required:**
    None
   
   **Optional:**
    None
    
* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{"sessionConfirmationNumber":-6957835531229764888}`
 
**Log user in** <a id="loginUser">
----
  Log in as a user. Note this is internal users only.
  Returns the repository id (userId) of the user if successfully authenticated.

* **URL**

  /atg/userprofiling/InternalProfileActor/login

* **Method:**

  `POST`
  
*  **Data Params**

   **Required:**
    `login=[string]` Username to log in with. <br />
    `password=[string]` Password to log in with. <br />
   
   **Optional:**
    None
    
* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{"userId":"portal-admin"}`
 
* **Error Response:**

  * **Code:** 409 <br />
    **Content:** `Your session expired due to inactivity`

  OR

  * **Code:** 200 <br />
    **Content:** `{"formError":true,"formExceptions":[{"localizedMessage":"The password is incorrect","errorCode":"invalidPassword"}]}`
 
**Log user out** <a id="logoutUser">
----
  Log out a user. Note this is internal users only.
  This makes the JSESSIONID no longer authenticated for a user.

* **URL**

  /atg/userprofiling/InternalProfileActor/logout

* **Method:**

  `POST`
  
*  **Data Params**

   **Required:**
    None
   
   **Optional:**
    None
    
* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{"atgResponse": "void"}`
 
* **Error Response:**

  * **Code:** 409 <br />
    **Content:** `Your session expired due to inactivity`


        