var activeProject = '';

$(document).ready(function () {

	/*
	 * **************************
	 * Top nav functions
	 * **************************
	 */
    $(".topnav li").click(function() {
      $(".active").removeClass('active');
      $(this).addClass('active');
    });
      
    // handle projects top menu item
    $("#projects").click(function() {
        $.getJSON( "/cgi-bin/controller/manageprojects.py?action=list_projects", function( data ) {
            var $pf = $('<form id="projectForm" method="get" action="#" ></form>');
            $pf.append('<p>Add new project</p>');
            $pf.append( '<button type="button" name="add_project" class="selectBtn" id="addproject" value="add_project">Add Project</button>');
            $pf.append('<p>Existing projects: </p>');
            $.each( data, function( key, val ) {
              if (activeProject == val) {
                  $pf.append( '<button type="button" class="selectedBtn" name="select_project" id="selectproject" value="' + val + '">Selected</button>' );
              } else {
                  $pf.append( '<button type="button" class="selectBtn" name="select_project" id="selectproject" value="' + val + '">Select Project</button>' );
              }
              $pf.append( '<button type="button" class="selectBtn" name="edit_project" id="editproject" value="' + val + '">Edit Project</button>' );
              $pf.append( '<button type="button" class="deleteBtn" name="delete_project" id="deleteproject" value="' + val + '">Delete Project</button>' );
              $pf.append( val + "<br/>");              
            });
            
            $( "#mainBody" ).empty();
            $pf.appendTo( "#mainBody" );
        });
    });
    
    // handle storage top menu item
    $("#storage").click(function() {
    	if (activeProject == '') {
    		errorData = {'status': 'error', 'message': 'No Project Selected ', 'errormsg': 'Select a project first'}
    		responseBox(errorData);
    		return;
    	}
        $.getJSON( "/cgi-bin/controller/manageprojects.py?action=list_storage&selected_project=" + activeProject, function( data ) {
            var $pf = $('<form id="storageForm" method="get" action="#" ></form>');
            $pf.append('<p>Add new storage</p>');
            $pf.append( '<button type="button" name="add_storage" class="selectBtn" id="addstorage" value="add_storage">Add Storage</button>');
            $pf.append('<p>Existing storage: </p>');
            $.each( data, function( key, val ) {
              $pf.append( '<button type="button" class="selectBtn" name="edit_storage" id="editstorage" value="' + val + '">Edit Storage</button>' );
              $pf.append( '<button type="button" class="deleteBtn" name="delete_storage" id="deletestorage" value="' + val + '">Delete Storage</button>' );
              $pf.append( val + "<br/>");              
            });
            
            $( "#mainBody" ).empty();
            $pf.appendTo( "#mainBody" );
        });
    });    
    
    // handle instances top menu item
    $("#instances").click(function() {
    	if (activeProject == '') {
    		errorData = {'status': 'error', 'message': 'No Project Selected ', 'errormsg': 'Select a project first'}
    		responseBox(errorData);
    		return;
    	}
        $.getJSON( "/cgi-bin/controller/manageprojects.py?action=list_instances&selected_project=" + activeProject, function( data ) {
            var $pf = $('<form id="instanceForm" method="POST" action="#" ></form>');
            $pf.append('<p>Add new instance</p>');
            $pf.append( '<button type="button" name="add_storage" class="selectBtn" id="addinstance" value="add_storage">Add Instance</button>');
            $pf.append('<p>Existing instances: </p>');
            $.each( data, function( key, val ) {
              $pf.append( '<button type="button" class="selectBtn" name="edit_instance" id="editinstance" value="' + val + '">Edit Instance</button>' );
              $pf.append( '<button type="button" class="deleteBtn" name="delete_instance" id="deleteinstance" value="' + val + '">Delete Instance</button>' );
              $pf.append( val + "<br/>");              
            });
            
            $( "#mainBody" ).empty();
            $pf.appendTo( "#mainBody" );
        });
    });   
    
    // handle gen configs top menu item
    $("#genconfigs").click(function() {
    	if (activeProject == '') {
    		errorData = {'status': 'error', 'message': 'No Project Selected ', 'errormsg': 'Select a project first'}
    		responseBox(errorData);
    		return;
    	}
        var $pf = $('<form id="genconfigForm" method="POST" action="#" ></form>');
        $pf.append('<p>Generate configurations and orchestrations</p>');
        $pf.append('<button type="button" name="generate_configs" class="selectBtn" id="generateconfigs" value="add_storage">Generate Configs</button>');
        
        $( "#mainBody" ).empty();
        $pf.appendTo( "#mainBody" );
    });      
    
    
    
	/*
	 * **************************
	 * Project related functions
	 * **************************
	 */    
    
    // get the fields to generate addproject form
    $('body').on('click', '#addproject', function() {
        var url = '/cgi-bin/controller/manageprojects.py?action=add_project_form';
        $.post( url, function( data ) {
            var $formContainer = $('<div class="form-container"></div>');
            var $form = $('<form id="project_add_form" action="/cgi-bin/controller/manageprojects.py?action=add_project" method="POST"></form>');
            $form.append( '<input type="hidden" name="action" value="add_project">');
            $.each( data, function( key, val ) {
                $form.append('<label>' + key + '</label>');        
                $form.append( '<input type="text" name="' + key + '">');
                $form.append('<br/>');  
            });
            $form.append('<button id="addProjectBtn" class="submitBtn">Add Project</button>');
            $( "#mainBody" ).empty();
            $formContainer.append($form);
            $formContainer.appendTo( "#mainBody" );
        });
    });
    
    // process the form to add a project
    $('body').on('click', '#addProjectBtn', function(event) {
        // get the form data
        var formData = {
            'new_project_name'       	: $('input[name=new_project_name]').val(),
            'opc_identity_domain'       : $('input[name=opc_identity_domain]').val(),
            'opc_username'              : $('input[name=opc_username]').val(),
            'opc_image_name'            : $('input[name=opc_image_name]').val(),
            'openstack_project_name'    : $('input[name=openstack_project_name]').val(),
            'openstack_image_name'      : $('input[name=openstack_image_name]').val(),
            'action' 					: 'add_project'
        };
    
        postData(formData).done(function(data) {
        	responseBox(data);
        	$( "#projects" ).click();
        });
        
        event.preventDefault();
    });      
    
    // get the fields to generate editproject form
    $('body').on('click', '#editproject', function() {
    	var project_name = $(this).attr("value");
        var url = '/cgi-bin/controller/manageprojects.py?action=edit_project_form&selected_project=' + project_name;
        
        $.post( url, function( data ) {
            var $formContainer = $('<div class="form-container"></div>');
            var $form = $('<form id="project_edit_form" action="/cgi-bin/controller/manageprojects.py" method="POST"></form>');
            $form.append( '<input type="hidden" name="new_project_name" value="' + project_name + '" >');
            $form.append( '<input type="hidden" name="action" value="edit_project">');
            $.each( data, function( key, val ) {
                $form.append('<label>' + key + '</label>'); 
                if (val == 'None') {
                	$form.append( '<input type="text" name="' + key + '" value="" >');
                } else {
                	$form.append( '<input type="text" name="' + key + '" value="' + val + '" >');
                }
                $form.append('<br/>');  
            });
            $form.append('<button id="updateProjectBtn" class="submitBtn">Update Project</button>');
            $( "#mainBody" ).empty();
            $formContainer.append("Editing Project: " + project_name);
            $formContainer.append($form);
            $formContainer.appendTo( "#mainBody" );
        });
    });    
    
    // process the update project form
    $('body').on('click', '#updateProjectBtn', function(event) {

    	// get the form data
        var formData = {
            'new_project_name'       	: $('input[name=new_project_name]').val(),
            'opc_identity_domain'       : $('input[name=opc_identity_domain]').val(),
            'opc_username'              : $('input[name=opc_username]').val(),
            'opc_image_name'            : $('input[name=opc_image_name]').val(),
            'openstack_project_name'    : $('input[name=openstack_project_name]').val(),
            'openstack_image_name'      : $('input[name=openstack_image_name]').val(),
            'action' 					: 'update_project'
        };
    
        postData(formData).done(function(data) {
        	responseBox(data);
        	$( "#projects" ).click();
        });
        
        event.preventDefault();
    });     
    
    $('body').on('click', '#selectproject', function() {
        var project_name = $(this).attr("value");
        activeProject = project_name;
        var url = '/cgi-bin/controller/manageprojects.py?action=select_project&selected_project=' + project_name;
        
        $.post( url, function( data ) {
            var parsed_data = JSON.parse(data);
            var $opc_details = $('<p>Active Project: ' + activeProject + '</p>');
            $opc_details.append("<br/>");
            $opc_details.append('OPC Domain Details:  ');
            // $opc_details.append("<br/>");
            var opc_data = parsed_data['opc'];
            $.each( opc_data, function( key, val ) {
              $opc_details.append( "<b>" + key + "</b>" + " = " + val + " ");              
            });
            var $os_details = $('<p></p>');
            $os_details.append('OpenStack Details:  ')
            //$os_details.append("<br/>");
            var os_data = parsed_data['openstack'];
            $.each( os_data, function( key, val ) {
              $os_details.append( "<b>" + key + "</b>" + " = " + val + " ");              
            });            
            $( "#info-container" ).empty();
            $opc_details.appendTo( "#info-container" );
            $os_details.appendTo( "#info-container" );
            $( "#projects" ).click();      
        });
              
    });
    
    $('body').on('click', '#deleteproject', function() {
        var project_name = $(this).attr("value");
        var formData = {
                'selected_project'       	: project_name,
                'action' 					: 'delete_project'
            };         
        
        postData(formData).done(function(data) {
        	responseBox(data);
        	$( "#projects" ).click();
        });     
    });      
    
    
	/*
	 * **************************
	 * Storage related functions
	 * **************************
	 */       
    // get the fields to generate addstorage form
    $('body').on('click', '#addstorage', function() {
        var url = '/cgi-bin/controller/manageprojects.py?action=add_storage_form';
        $.post( url, function( data ) {
            var $formContainer = $('<div class="form-container"></div>');
            var $form = $('<form id="storage_add_form" action="/cgi-bin/controller/manageprojects.py?action=add_storage&selected_project=' + activeProject + ' method="POST"></form>');
            $form.append( '<input type="hidden" name="action" value="add_storage">');
            $.each( data, function( key, val ) {
            	if (key == 'radio') {
            		$form.append('<label class="radiodivlabel">' + 'properties' + '</label>');
            		var $radiodiv = $('<div class="radiodiv">');
            		
            		$.each( data.radio, function (k, v) {       
            			if (k == '/oracle/public/storage/default') {
            				$radiodiv.append( '<input class="radioinput" type="radio" name="properties" checked="checked" value="' + k + '">');
            				$radiodiv.append( '<label class="radiolabel">' + k + '</label>');
            				$radiodiv.append('<br/>')           				
            			} else {
            				$radiodiv.append( '<input class="radioinput" type="radio" name="properties" value="' + k + '">');
            				$radiodiv.append( '<label class="radiolabel">' + k + '</label>');
            				$radiodiv.append('<br/>');
            			}
            		});
            		$form.append($radiodiv);
            		$form.append('<br/>');
            	} else {
	                $form.append('<label>' + key + '</label>');        
	                $form.append( '<input type="text" name="' + key + '">');
	                $form.append('<br/>');
            	}
            });
            $form.append('<button id="addStorageBtn" class="submitBtn">Add Storage</button>');
            $( "#mainBody" ).empty();
            $formContainer.append($form);
            $formContainer.appendTo( "#mainBody" );
        });
    });    
    
    // process the form to add storage
    $('body').on('click', '#addStorageBtn', function(event) {
        // get the form data
        var formData = {
        	'selected_project'  : activeProject,
        	'name'       		: $('input[name=name]').val(),
            'properties'        : $('input[name=properties]:checked').val(),
            'description'       : $('input[name=description]').val(),
            'size'            	: $('input[name=size]').val(),
            'action' 			: 'add_storage'
        };
    
        postData(formData).done(function(data) {
        	responseBox(data);
        	$( "#storage" ).click();
        });
        
        event.preventDefault();
    });      

    // get the fields to generate editstorage form
    $('body').on('click', '#editstorage', function() {   	
        var storage_name = $(this).attr("value");
        var formData = {
                'selected_project'       	: activeProject,
                'selected_storage'          : storage_name,
                'action' 					: 'edit_storage_form'
            };        

        postData(formData).done(function(data) {
            var $formContainer = $('<div class="form-container"></div>');
            var $form = $('<form id="storage_edit_form" action="/cgi-bin/controller/manageprojects.py" method="POST"></form>');
            $form.append( '<input type="hidden" name="selected_project" value="' + activeProject + '" >');
            $form.append( '<input type="hidden" name="action" value="edit_storage">');
            $form.append('<label>name (readonly)</label>');

            $form.append( '<input type="text" name=name value="' + data.name + '" readonly>');
            $form.append('<br/>');
            
            $form.append('<label>description</label>');
            if (data.description == 'None') {
            	$form.append( '<input type="text" name="description" value="" >');
            } else {
            	$form.append( '<input type="text" name="description" value="' + data.description + '" >');
            }   
            $form.append('<br/>');
           
            $form.append('<label class="radiodivlabel">' + 'properties' + '</label>');
            var $radiodiv = $('<div class="radiodiv">');
            
            if (data.properties == '/oracle/public/storage/default') {
            	$radiodiv.append( '<input class="radioinput" type="radio" name="properties" checked="checked" value="/oracle/public/storage/default">');
            	$radiodiv.append( '<label class="radiolabel">' + '/oracle/public/storage/default' + '</label>');
            	$radiodiv.append('<br/>')  
            } else {
            	$radiodiv.append( '<input class="radioinput" type="radio" name="properties" value="/oracle/public/storage/default">');
            	$radiodiv.append( '<label class="radiolabel">' + '/oracle/public/storage/default' + '</label>');
            	$radiodiv.append('<br/>')
            }     
            if (data.properties == '/oracle/public/storage/latency') {
            	$radiodiv.append( '<input class="radioinput" type="radio" name="properties" checked="checked" value="/oracle/public/storage/latency">');
            	$radiodiv.append( '<label class="radiolabel">' + '/oracle/public/storage/latency' + '</label>');
            	$radiodiv.append('<br/>')  
            } else {
            	$radiodiv.append( '<input class="radioinput" type="radio" name="properties" value="/oracle/public/storage/latency">');
            	$radiodiv.append( '<label class="radiolabel">' + '/oracle/public/storage/latency' + '</label>');
            	$radiodiv.append('<br/>')
            }              
            $form.append($radiodiv);
            $form.append('<br/>');
            
            $form.append('<label>size</label>');
            if (data.size == 'None') {
            	$form.append( '<input type="text" name=size value="" >');
            } else {
            	$form.append( '<input type="text" name=size value="' + data.size + '" >');
            }            
            $form.append('<br/>');
            
            $form.append('<button id="updateStorageBtn" class="submitBtn">Update Storage</button>');
            $( "#mainBody" ).empty();
            $formContainer.append("Editing Storage: " + storage_name);
            $formContainer.append($form);
            $formContainer.appendTo( "#mainBody" )            
        });
        
    });
    
    // process the update storage form
    $('body').on('click', '#updateStorageBtn', function(event) {

    	// get the form data
        var formData = {
            'selected_project'  : activeProject,
            'name'       		: $('input[name=name]').val(),
            'properties'        : $('input[name=properties]:checked').val(),
            'description'       : $('input[name=description]').val(),
            'size'            	: $('input[name=size]').val(),
            'action' 			: 'update_storage'
            };
    
        postData(formData).done(function(data) {
        	responseBox(data);
        	$( "#storage" ).click();
        });
        
        event.preventDefault();
    });       
        
    $('body').on('click', '#deletestorage', function() {
        var storage_name = $(this).attr("value");
        var formData = {
                'selected_project'       	: activeProject,
                'selected_storage'          : storage_name,
                'action' 					: 'delete_storage'
            };        

        postData(formData).done(function(data) {
        	responseBox(data);
        	$( "#storage" ).click();
        });
            
    });        

	/*
	 * **************************
	 * Instance related functions
	 * **************************
	 */

    $('body').on('click', '#deleteinstance', function() {
        var instance_name = $(this).attr("value");
        var formData = {
                'selected_project'       	: activeProject,
                'selected_instance'          : instance_name,
                'action' 					: 'delete_instance'
            };        

        postData(formData).done(function(data) {
        	responseBox(data);
        	$( "#instances" ).click();
        });
            
    }); 
    
    $('body').on('click', '#editinstance', function() {
    	var response_data = {'status': 'success', 'message': 'Feature not enabled'}
        responseBox(response_data);
    });     

    // get the fields to generate the first addinstance form - instance type and platform
    $('body').on('click', '#addinstance', function() {
        var url = '/cgi-bin/controller/manageprojects.py?action=add_instance_form';
        $.post( url, function( data ) {
            var $formContainer = $('<div class="form-container"></div>');
            var $form = $('<form id="instance_add_form"></form>');
            $form.append( '<input type="hidden" name="action" value="set_instance_type">');
            $form.append("Select software to install/configure on this instance: ");
            var $instance_types_div = $('<div class="instance_types_div">');
            $.each( data, function( key, val ) {
            	$instance_types_div.append('<label class="instance_types_label">' + key + '</label>');        
            	$instance_types_div.append('<input class="instance_types_checkbox" type="checkbox" name="instancetypes" value="' + val + '">');
            	$instance_types_div.append('<br/>');
            });
            $form.append($instance_types_div);
            $form.append('<br/>'); 
            
            $form.append("Select target platform for this instance: ");
            var $target_platform_div = $('<div class="target_platform_div">');
            $target_platform_div.append('<label class="instance_types_label">Oracle Public Cloud</label>');        
            $target_platform_div.append('<input class="instance_types_checkbox" type="radio" checked="checked" name="targetplatform" value="opc">');
            $target_platform_div.append('<br/>');
            $target_platform_div.append('<label class="instance_types_label">OpenStack</label>');        
            $target_platform_div.append('<input class="instance_types_checkbox" type="radio" name="targetplatform" value="openstack">');
            $target_platform_div.append('<br/>');           
            $form.append($target_platform_div);
            
            $form.append("Select JSON config data source: ");
            var $configsource_div = $('<div id="configsource_div" class="instance_types_div">');
            $configsource_div.append('<label class="instance_types_label">Default Embedded JSON</label>');        
            $configsource_div.append('<input class="instance_types_checkbox" type="radio" checked="checked" name="configsource" value="defaultjson">');
            $configsource_div.append('<br/>');
            $configsource_div.append('<label class="instance_types_label">Instance meta data</label>');        
            $configsource_div.append('<input class="instance_types_checkbox" type="radio" name="configsource" value="metadata">');
            $configsource_div.append('<br/>');  
            $configsource_div.append('<label class="instance_types_label">Local file</label>');        
            $configsource_div.append('<input class="instance_types_checkbox" type="radio" name="configsource" value="configfile">');
            $configsource_div.append('<br/>');             
            $configsource_div.append('<label class="instance_types_label">HTTP endpoint</label>');        
            $configsource_div.append('<input class="instance_types_checkbox" id="remotedataradio" type="radio" name="configsource" value="remotedata">');

            var $meta_config_div = $('<div id="meta_config_div" style="display:none;">');
            $meta_config_div.append('<br/>');
            $meta_config_div.append('<label class="textarea_label">Enter user meta-data</label>');
            $meta_config_div.append('<textarea type="text" id="usermetadata" name="usermetadata">');
            $configsource_div.append($meta_config_div);
            
            var $remote_config_div = $('<div id="remote_config_div" style="display:none;">');
            $remote_config_div.append('<br/>');
            $remote_config_div.append('<label class="instance_types_label">Enter endpoint</label>');
            $remote_config_div.append('<input type="text" id="remotedataaddress" name="remotedataaddress" value="" >');
            $configsource_div.append($remote_config_div);
            
            var $file_config_div = $('<div id="file_config_div" style="display:none;">');
            $file_config_div.append('<br/>');
            $file_config_div.append('<label class="instance_types_label">Enter filename</label>');
            $file_config_div.append('<input type="text" id="configfilename" name="configfilename" value="" >');
            $configsource_div.append($file_config_div);            
            
            $configsource_div.append('<br/>');                          
            $form.append($configsource_div);            
        	            
            $form.append('<br/>'); 
            $form.append('<button id="getInstanceFieldsBtn" class="submitBtn">Continue</button>');
            $( "#mainBody" ).empty();
            $formContainer.append($form);
            $formContainer.appendTo( "#mainBody" );
        });
    });    
    
    // watch the configsource radio and show text field when source is changed
    $('body').on('change', "input[name='configsource']", function() {
    	   
    	if($(this).val()=="remotedata")
    	{
    		$("#file_config_div").hide();
    		$("#meta_config_div").hide();
    	    $("#remote_config_div").show();
    	} else if ($(this).val()=="configfile") {
    		$("#remote_config_div").hide();
    		$("#meta_config_div").hide();
    		$("#file_config_div").show();
    	}
    	else if ($(this).val()=="metadata") {
    		$("#remote_config_div").hide();
    		$("#file_config_div").hide();
    		$("#meta_config_div").show();
    	}    	
    	else
    	{
    	    $("#remote_config_div").hide();
    	    $("#file_config_div").hide();
    	    $("#meta_config_div").hide();
    	}
    	    
    });
             

    // get the fields to generate the second addinstance form 
    function add_instance_form2(data) {
    	
        var $formContainer = $('<div class="form-container"></div>');
        var $form = $('<form id="instance_add_form2" action="/cgi-bin/controller/manageprojects.py method="POST"></form>');
        $form.append( '<input type="hidden" name="action" value="add_instance">');
        
        var $instance_type_info = $('<div class="instance_type_info">');
        $instance_type_info.append('<label class="instance_type_info_label">Instance types:' + data.instance_types + '</label>');
        $instance_type_info.append('<input type="hidden" name="instance_types" value="' + data.instance_types + '">');
        $instance_type_info.append('<br/>'); 
        $instance_type_info.append('<label>Target platform:' + data.target_platform + '</label>');
        $instance_type_info.append('<input type="hidden" name="target_platform" value="' + data.target_platform + '">');
        $instance_type_info.append('<br/>'); 
        $instance_type_info.append('<label>Config source:' + data.config_source + '</label>');
        $instance_type_info.append('<input type="hidden" name="config_source" value="' + data.config_source + '">');        
        $form.append($instance_type_info);
        
        $form.append("Enter instance data: ");
        var $instance_data_div = $('<div class="instance_data_div">');
        $.each( data.instance_fields, function( key, val ) {
        	$instance_data_div.append('<label class="instance_types_label">' + val + '</label>');        
        	$instance_data_div.append('<input type="text" name="' + val + '" value="" >');
        	$instance_data_div.append('<br/>');
        });
        $form.append($instance_data_div);
        $form.append('<br/>'); 
        
        $form.append("Enter required fields: ");
        var $required_data_div = $('<div id="required_data_div" class="required_data_div">');
        $.each( data.required_fields, function( key, val ) {
        	$required_data_div.append('<label class="section_label">Section: ' + key + '</label>');
        	if (isArray(val)) {
        		var divId = key + '_array_div';
        		var $array_data_div = $('<div id="' + divId + '" class="array_div">');
        		$required_data_div.append('<label class="repeat_label">array</label>');
        		$required_data_div.append('<br/>');
                $.each( val[0], function( arrkey, arrval ) {        	
                	$array_data_div.append('<label class="subsection_input_label">' + arrkey + ' ' + arrval[0] + '</label>');
                	$array_data_div.append('<input type="text" name="' + arrkey + '" placeholder="' + arrval[1] + '" >');
                	$array_data_div.append('<br/>');      		                	
                });	    
                var $add_more = ('<button id="cloneDiv" class="submitBtn" name="' + divId +'">Add Fields</button>');
                $array_data_div.append($add_more);
                $array_data_div.append('<br/>'); 
                $required_data_div.append($array_data_div);

        		
        	} else {
        		// if not an array, use shared function to create inputs
        		var $nesteddata = build_required_data(key,val);
        		$required_data_div.append($nesteddata);
        	}
        	$required_data_div.append('<br/>');
        });
        $form.append($required_data_div);
        $form.append('<br/>');  
        
        $form.append("Enter Optional fields: ");
        $form.append('<br/>');
        $form.append("Click the button corresponding to the data type you wish to add");
        var $optional_data_wrapper_div = $('<div id="optional_data_div" class="optional_data_div">');
        var $optional_button_container = $('<empty>');
        $.each( data.optional_fields, function( key, val ) {
        	var $add_optional_button = ('<button id="addOptionalField" class="optionalSubmitBtn" name="' + key +'">Add ' + key + '</button>');
        	$optional_button_container.append($add_optional_button);
        	if (isArray(val)) {
        		var $optional_data_div = $('<div id="' + key + '" style="display:none;" class="optional_data_div disabled">');
        		$optional_data_div.append('<label class="section_label">Section: ' + key + '</label></br>');
        		var divId = key + '_array_div';
        		var $array_data_div = $('<div id="' + divId + '" class="array_div">');
        		$optional_data_div.append('<br/>');
                $.each( val[0], function( arrkey, arrval ) {
            		$array_data_div.append('<label class="subsection_input_label">' + arrkey + ' ' + arrval[0] + '</label>');
            		$array_data_div.append('<input type="text" name="' + arrkey + '" placeholder="' + arrval[1] + '" >');
            		$array_data_div.append('<br/>');
                });	    
                var $add_more = ('<button id="cloneDiv" class="submitBtn" name="' + divId +'">Add More Fields</button>');
                $array_data_div.append($add_more);
                $array_data_div.append('<br/>'); 
                $optional_data_div.append($array_data_div);
                $optional_data_div.append('<br/>');
        		
        	} else {
        		// if not an array, use shared function to create inputs
        		var $nesteddata = build_required_data(key,val);
        		$nesteddata.prepend('<label class="section_label">Section: ' + key + '</label></br>');
        		$nesteddata.addClass('disabled');
        		$nesteddata.hide();
        		
        		$optional_data_wrapper_div.append($nesteddata);
        		$optional_data_wrapper_div.append('<br/>');
        	}
        	$optional_data_wrapper_div.append($optional_data_div);
        });
        $optional_data_wrapper_div.append($optional_button_container);
        $form.append($optional_data_wrapper_div);
        $form.append('<br/>');         
        
        $form.append('<button id="addInstanceBtn" class="submitBtn">Add Instance</button>');
        $( "#mainBody" ).empty();
        $formContainer.append($form);
        $formContainer.appendTo( "#mainBody" );
    }; 
    
    function build_required_data(typekey, dataval) {
    	var $html_to_return = $('<div id=' + typekey + '>');
        $.each( dataval, function( key, val ) {    
        	// ignore the required json template indicator
        	if (key == "required") {
        		return;
        	}
        	if (isArray(val)) {
	        	$html_to_return.append('<label class="subsection_input_label">' + key + ' ' + val[0] + '</label>');
	        	$html_to_return.append('<input type="text" name="' + key + '" placeholder="' + val[1] + '" >');
	        	$html_to_return.append('<br/>');      		
        	} else {
        		var $sub_html = $('<div id=' + key + '>');
        		$sub_html.append('<label class="subsection_label">Sub Section: ' + key + '</label>');        
        		$sub_html.append('<br/>');        		
        		$.each( val, function( subkey, subval ) {
        			$sub_html.append('<label class="subsection_input_label">' + subkey + ' ' + subval[0] + '</label>');  
        			$sub_html.append('<input type="text" name="' + subkey + '" placeholder="' + subval[1] + '" >');
        			$sub_html.append('<br/>');        			
        		})
        		$html_to_return.append($sub_html);
        	}
        });	
        
        return $html_to_return;
    }

    // process attach storage button
    $('body').on('click', '#attachStorage', function(event) {
    	
        event.preventDefault();
    }); 
    
    // process add optional field button
    $('body').on('click', '#addOptionalField', function(event) {
    	var fields_to_show = $(this).attr("name");
    	
    	// remove the disabled class
    	$('#' + fields_to_show).removeClass("disabled");
    	// show the div corresponding to the button clicked
    	$('#' + fields_to_show).show();

    	
    	// hide the original button clicked now that the fields are there
    	$('#addOptionalField[name="' + fields_to_show + '"]').hide();
    	
        event.preventDefault();
    }); 
    
    // process clone div button
    $('body').on('click', '#cloneDiv', function(event) {
    	var div_to_clone = $(this).attr("name");
    	
    	// get the last instance of our div we are cloning
    	var $last_cloned_div = $('div[id^="' + div_to_clone + '"]:last');
    	var num;
    	if ($last_cloned_div.length !== 0) {
    		// see if a number is already on the end of the id. increment if so
    		num = parseInt( $last_cloned_div.prop("id").match(/\d+/g), 10 ) +1;	
    	}
    	// if no num was present, we'll get NaN. Just set to 1
    	if (isNaN(num)) {
    		num = 1;
    	}
    	
    	// make a clone of the original div
    	var $cloned_div = $("#" + div_to_clone).clone().prop('id', div_to_clone + num); 
    	
    	// number our atgServerType radios if they exist
    	$cloned_div.find("input[name=atgServerType]").each(function(index, element) {
    		this.name = "atgServerType" + num;
    		$(this).prop("checked",false);
    	});
    	
    	// get rid of the remove button from previous blocks
    	$last_cloned_div.find("#removeDiv").remove();
    	var $remove_div = ('<button id="removeDiv" class="submitBtn" name="' + div_to_clone + num +'">Delete Fields</button>');
    	$cloned_div.append($remove_div);
    	
    	$last_cloned_div.after($cloned_div);
    	$last_cloned_div.after("<br/>");
        event.preventDefault();
    }); 
    
    // process remove div button
    $('body').on('click', '#removeDiv', function(event) {
    	var div_to_remove = $(this).attr("name");
    	$("#" + div_to_remove).remove();
    	
    	div_to_remove = div_to_remove.slice(0,-1)
    	var $last_cloned_div = $('div[id^="' + div_to_remove + '"]:last');
    	var num;
    	if ($last_cloned_div.length !== 0) {
    		// see if a number is already on the end of the id
    		num = parseInt( $last_cloned_div.prop("id").match(/\d+/g), 10 );	
    	}
    	// if no num was present, return. no deleting the top level block
    	if (isNaN(num)) {
    		return;
    	}    	
    	var $remove_div = ('<button id="removeDiv" class="submitBtn" name="' + $last_cloned_div.attr("id") +'">Delete Fields</button>');
    	$last_cloned_div.append($remove_div);    	
        event.preventDefault();
    });  
    
    // process addInstanceBtn button
    $('body').on('click', '#addInstanceBtn', function(event) {

    	var instance_data_json = {};
    	    	
    	// get all the required and optional fields based on instance type selected
    	$("#required_data_div,#optional_data_div").children('div').each(function () {
    		var divid = $(this).attr("id");
    		var isArrayDiv = false;

    		// skip any div blocks marked as disabled
    		if ($(this).hasClass("disabled")) {
    			return;
    		}
    		
    		if (divid.indexOf('_array_div') !== -1) {
    			isArrayDiv = true;
    		} 
    		//chop off array_div so we just have the field type in the ID
    		divid = divid.replace(/_array_div.*/, '');
    		var returned_raw = getAllInputs($(this), isArrayDiv);
    		if (isObject(instance_data_json[divid])) {
    			instance_data_json[divid].push(returned_raw[0]);
    		} else {
    			instance_data_json[divid] = returned_raw;
    		}    		
    	});
    	 	
    	    	        	
    	// get the form data
        var formData = {
            'instance_name'    	: $('input[name=instance_name]').val(),
            'hostname'    		: $('input[name=hostname]').val(),
            'sshkey_name'    	: $('input[name=sshkey_name]').val(),
            'opc_shape'    		: $('input[name=opc_shape]').val(),
            'openstack_flavor'  : $('input[name=openstack_flavor]').val(),
            'instance_types'  	: $('input[name=instance_types]').val(),
            'target_platform'  	: $('input[name=target_platform]').val(),
            'json_blob'  		: JSON.stringify(instance_data_json),
            'selected_project'  : activeProject,
            'action' 		   	: 'add_instance'
            };
            
        // only hold defaultjson for the user to see a value. We don't actually use it.
        config_source = $('input[name=config_source]').val();
        if (config_source == "defaultjson") {
        	config_source = ""; 
        }
        
        formData['config_source'] = config_source;
                
        postData(formData).done(function(data) {        
        	responseBox(data);
        	if (data['status'] == 'success') {
        		$( "#instances" ).click();
        	}
        });
        
        event.preventDefault();
    });       
    
    // get the values of all input fields, and build json based on nested divs
    function getAllInputs($data, isArrayDiv) {
		
		var divid = $data.attr("id");
		// hold key value input pairs
		var field_holder = {};
		var return_data = {};
				
		// get immediate child inputs only, that are not marked disabled
		$data.find('> input:not(:disabled)').each(function() {
			var field_name = $(this).attr("name");
			var field_value;
			
			if ($(this).is(':radio')) {			
				field_holder = $('input[name=' + field_name +']:checked').val()
			} else {
				if ($(this).val()) {
					field_value = $(this).val();
					
				} else {
					// if they didn't enter a value, use the placeholder
					field_value = $(this).attr("placeholder");
				}
				
				field_holder[field_name] = field_value;
			}						
		});

		return_data = field_holder;
		
		// if array divs, we need to hold outside the loop
		var arrayHolder = [];
		//var radioHolder = {};
		
		// if this div has children divs, go through them
		$data.children('div').each(function () {

			var localdivid = $(this).attr("id");
    		var localIsArrayDiv = false;
			
    		if (localdivid.indexOf('_array_div') !== -1) {
    			localIsArrayDiv = true;
    			arrayHolder.push(getAllInputs($(this), localIsArrayDiv));
    		} else {
    			return_data[localdivid]= getAllInputs($(this), localIsArrayDiv);
    		}
		});
		
		if (arrayHolder.length !== 0) {
			return_data = arrayHolder;
		}

		return return_data;
    }
    
    function isArray(o) {
    	  return Object.prototype.toString.call(o) === '[object Array]';
    }  
    
    function isObject(x) {
  	  return (typeof x === 'object') && (x !== null);
  }       

    // process first instance form
    $('body').on('click', '#getInstanceFieldsBtn', function(event) {

    	// get the form data
        var formData = {
            'targetplatform'    : $('input[name=targetplatform]:checked').val(),
            'action' 			: 'set_instance_type'
            };
        
        var checkedValues = $('input[name="instancetypes"]:checked').map(function() {
            return this.value;
        }).get();
        
        var configsource = $('input[name="configsource"]:checked').val();
        var configsource_value;
                
        if (configsource == 'metadata') {
        	configsource_value = $('input[name=usermetadata]').val();
        } else if (configsource == 'configfile') {
        	configsource_value = 'file:' + $('input[name=configfilename]').val();
        } else if (configsource == 'remotedata') {
        	configsource_value = $('input[name=remotedataaddress]').val();
        } else if (configsource == 'defaultjson') {
        	configsource_value = "defaultjson";
        }
        
        formData['instancetypes'] = checkedValues;
        formData['configsource'] = configsource_value;
    
        postData(formData).done(function(data) {
        	add_instance_form2(data);
        });
        
        event.preventDefault();
    }); 

	/*
	 * **************************
	 * Config related functions
	 * **************************
	 */
    // generate configs/orchs
    $('body').on('click', '#generateconfigs', function(event) {

    	// get the form data
        var formData = {
            'selected_project'  : activeProject,
            'action' 			: 'generate_configs'
            };
    
        postData(formData).done(function(data) {
        	responseBox(data);
        });
        
        event.preventDefault();
    }); 
    
	/*
	 * **************************
	 * Shared functions
	 * **************************
	 */
    
    function responseBox(msg_data) {
        if (msg_data['status'] == 'success') {
            $("<div>" + msg_data['message'] + "</div>").dialog();             
        } else {
            $("<div id='#dialog' title='" + msg_data['message'] + "'>" + msg_data['errormsg'] + "</div>").dialog({modal: true}).parent().addClass("ui-state-error");                  
        }
    }    
    
    function postData(data_to_post) {
    	myUrl = '/cgi-bin/controller/manageprojects.py';
        return $.ajax({
            type        : 'POST', 
            url         : myUrl, 
            data        : data_to_post,
            dataType    : 'json',
            encode      : true
        });    
    }
     
});