ansible-playbook playbooks/seclist/seclist.yaml > logs/seclist.log  2>&1
ansible-playbook playbooks/secapp/secapp.yaml > logs/secapp.log  2>&1
ansible-playbook playbooks/storage/atgdb_storage_storage.yaml > logs/atgdb_storage_storage.log  2>&1
ansible-playbook playbooks/storage/atg_install_storage_storage.yaml > logs/atg_install_storage_storage.log  2>&1
ansible-playbook playbooks/storage/wls_install_storage_storage.yaml > logs/wls_install_storage_storage.log  2>&1
ansible-playbook playbooks/instances/endeca1_instance.yaml > logs/endeca1_instance.log  2>&1 &
ansible-playbook playbooks/instances/endeca2_instance.yaml > logs/endeca2_instance.log  2>&1 &
ansible-playbook playbooks/instances/atg1_instance.yaml > logs/atg1_instance.log  2>&1 &
ansible-playbook playbooks/instances/atg2_instance.yaml > logs/atg2_instance.log  2>&1 &
ansible-playbook playbooks/instances/atgsupport_instance.yaml > logs/atgsupport_instance.log  2>&1 &
ansible-playbook playbooks/instances/otd_instance.yaml > logs/otd_instance.log  2>&1 &
ansible-playbook playbooks/instances/atgdb_instance.yaml > logs/atgdb_instance.log  2>&1 &
