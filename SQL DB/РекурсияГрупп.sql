
with recursive catalog_pas as (
	select 
		id , name, parent_id
	from 
		msa_config_management.catalog_node
	where id = 'a272dd09-dca3-4767-9f93-a06e8929222c'
	
	union all
	
	select 
		N.id , N.name, N.parent_id
	from 
		msa_config_management.catalog_node as N
	inner join 
		msa_config_management.catalog_node root on N.parent_id = root.id
) select * from catalog_pas