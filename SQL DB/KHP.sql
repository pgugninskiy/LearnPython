select 
	count(1)
	, h.conf_type
	, h.name
	, h.id
from msa_config_management.conf_header h inner join msa_config_management.conf_version v on h.id = v.configuration_id  and v.version_type = 'DRAFT'
group by h.id 
having count(1)>1
order by 2,3;

select * 
from msa_config_management.conf_header as H
join msa_config_management.conf_link as L 
	on H.id  = L.conf_id 
join msa_config_management.catalog_node as N
	on L.node_id = N.id 
where H.id IN ('b57cf5db-43fa-49b1-aafd-ac76c3daeb84' , '8042bb10-42d8-4fd3-bd5d-732b19c90c53' , '17b315d8-279b-4c41-824d-d63df4bb1b73')

select * 
from msa_config_management.conf_version as V
where V.configuration_id  IN ('b57cf5db-43fa-49b1-aafd-ac76c3daeb84' , '8042bb10-42d8-4fd3-bd5d-732b19c90c53' , '17b315d8-279b-4c41-824d-d63df4bb1b73')




select h."name", n."name", r.related_conf_id  
from msa_config_management.catalog_node as N
join msa_config_management.conf_link as L
 	on l.node_id = N.id 
join msa_config_management.conf_header as H
	on h.id = l.conf_id 
join msa_config_management.relation as r
	on r.conf_id = h.id 
where n.id in ('7563239b-85b3-4eef-b7eb-0d51546d704a' , '1e94b5ea-9fa8-4d37-9f5e-7914bb6fd493' , 'a272dd09-dca3-4767-9f93-a06e8929222c' , 'cecef126-fa9a-42f6-98a0-2d291106eaf7')




r.conf_id, h."name" , r.related_conf_id, n."name"  
from msa_config_management.relation r
join msa_config_management.conf_link as L 
	on r.conf_id  = L.conf_id 
join msa_config_management.catalog_node as N
	on L.node_id = N.id
join msa_config_management.conf_header as H
	on r.conf_id = H.id 
where n.id in ('7563239b-85b3-4eef-b7eb-0d51546d704a' , '1e94b5ea-9fa8-4d37-9f5e-7914bb6fd493' , 'a272dd09-dca3-4767-9f93-a06e8929222c' , 'cecef126-fa9a-42f6-98a0-2d291106eaf7') 

