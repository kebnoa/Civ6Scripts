civicNodesQueryString = """\
select CivicType
     , Name
	 , Cost
	 , 'C'
	 , EraType
	 , 'Civic'
  from Civics"""
civicEdgesQueryString = """\
select PrereqCivic
     , Civic
	 , 'Civic'
  from CivicPrereqs"""
techNodesQueryString = """\
select TechnologyType
     , Name
	 , Cost
	 , 'S'
	 , EraType
	 , 'Technology' 
  from Technologies"""
techEdgesQueryString = """
select PrereqTech
     , Technology
	 , 'Technology'
  from TechnologyPrereqs"""
# Stripped out the Civilization Unique Districts to simplify the graph
# Also chance City Centre to cost 0? (DB has it as 54P?)
districtNodesQueryString = """\
select d.DistrictType
     , d.Name
	 , case DistrictType
	      when 'DISTRICT_CITY_CENTER' then 0
		  else d.Cost
	   end as Cost
     , 'P'
     , case coalesce(t.EraType, '') || coalesce(c.EraType, '')
	      when '' then 'ERA_ANCIENT' 
	      else coalesce(t.EraType, '') || coalesce(c.EraType, '')
       end as EraType
     , 'District'
  from Districts d 
       left join Technologies t
           on d.PrereqTech = t.TechnologyType
	   left join Civics c
           on d.PrereqCivic = c.CivicType
	   left join DistrictReplaces dr
	       on d.DistrictType = dr.CivUniqueDistrictType
 where d.InternalOnly != 1
   and dr.CivUniqueDistrictType is null"""
districtEdgesQueryString = """\
select case coalesce(PrereqTech, '') || coalesce(PrereqCivic, '')
           when '' then 'SETTLE_FIRST_CITY'
		   else coalesce(PrereqTech, '') || coalesce(PrereqCivic, '')
	   end as Prereq
	 , DistrictType
	 , 'District'
  from Districts d
       left join DistrictReplaces dr
	       on d.DistrictType = dr.CivUniqueDistrictType
 where InternalOnly != 1
   and dr.CivUniqueDistrictType is null"""
wonderNodesQueryString = """\
select b.BuildingType
     , b.Name
	 , b.Cost
     , 'P'
     , case coalesce(t.EraType, '') || coalesce(c.EraType, '')
          when '' then 'ERA_ANCIENT' 
	      else coalesce(t.EraType, '') || coalesce(c.EraType, '')
       end as EraType
	 , 'Wonder'
  from Buildings b
       left join Technologies t
           on b.PrereqTech = t.TechnologyType
	   left join Civics c
           on b.PrereqCivic = c.CivicType
 where b.IsWonder = 1"""
wonderEdgesQueryString = """\
select coalesce(PrereqTech, '') || coalesce(PrereqCivic, '') as Prereq
     , BuildingType
	 , 'Wonder'
  from Buildings
 where IsWonder = 1"""
# Stripped out the Civilization Unique Buildings to simplify the graph.
buildingNodesQueryString = """\
select b.BuildingType
     , b.Name
	 , b.Cost
	 , 'P'
	 , case coalesce(c.EraType, '') || coalesce(t.EraType, '') 
          when '' then 
			 case b.BuildingType 
		         when 'BUILDING_MONUMENT' then 'ERA_ANCIENT'
			     when 'BUILDING_PALACE' then 'ERA_ANCIENT'
			     else 'ERA_CLASSICAL'
			 end
		  else coalesce(t.EraType, '') || coalesce(c.EraType, '') 
	    end as EraType
	  , 'Building'
  from Buildings b
       left join Civics c
	      on b.PrereqCivic = c.CivicType
	   left join Technologies t
	      on b.PrereqTech = t.TechnologyType
	   left join BuildingReplaces br
	      on b.BuildingType = br.CivUniqueBuildingType
 where IsWonder = 0
       and InternalOnly = 0
	   and UnlocksGovernmentPolicy = 0
	   and br.CivUniqueBuildingType is null"""
buildingEdgesQueryString = """\
select case coalesce(b.PrereqTech, '') || coalesce(b.PrereqCivic, '') 
          when '' then 
			 case b.BuildingType 
		         when 'BUILDING_MONUMENT' then 'DISTRICT_CITY_CENTER'
			     when 'BUILDING_PALACE' then 'DISTRICT_CITY_CENTER'
			     else 'BUILDING_TEMPLE'
			 end
		  else coalesce(b.PrereqTech, '') || coalesce(b.PrereqCivic, '') 
	  end as Prereq
     , b.BuildingType
	 , 'Building'
  from Buildings b
       left join BuildingReplaces br
	      on b.BuildingType = br.CivUniqueBuildingType
 where IsWonder = 0
       and InternalOnly = 0
	   and UnlocksGovernmentPolicy = 0
	   and br.CivUniqueBuildingType is null
union
select bp.PrereqBuilding as Prereq
     , bp.Building as BuildingType
	 , 'Building'
  from BuildingPrereqs bp
       left join Buildings b
	      on bp.Building = b.BuildingType
	   left join BuildingReplaces br
	      on bp. Building = br.CivUniqueBuildingType
 where b.IsWonder = 0
       and br.CivUniqueBuildingType is null"""