-- CS4400: Introduction to Database Systems (Fall 2022)
-- Project Phase III: Stored Procedures SHELL [v0] Monday, Oct 31, 2022
set global transaction isolation level serializable;
set global SQL_MODE = 'ANSI,TRADITIONAL';
set names utf8mb4;
set SQL_SAFE_UPDATES = 0;

use restaurant_supply_express;
-- -----------------------------------------------------------------------------
-- stored procedures and views
-- -----------------------------------------------------------------------------
/* Standard Procedure: If one or more of the necessary conditions for a procedure to
be executed is false, then simply have the procedure halt execution without changing
the database state. Do NOT display any error messages, etc. */

-- [1] add_owner()
-- -----------------------------------------------------------------------------
/* This stored procedure creates a new owner.  A new owner must have a unique
username.  Also, the new owner is not allowed to be an employee. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_owner;
delimiter //
create procedure add_owner (in ip_username varchar(40), in ip_first_name varchar(100),
	in ip_last_name varchar(100), in ip_address varchar(500), in ip_birthdate date)
sp_main: begin
    if ((ip_username in (select username from users)) or 
    (ip_username in (select username from employees)))
    then leave sp_main; end if;
    insert into users values (ip_username, ip_first_name, ip_last_name, ip_address, ip_birthdate);
    insert into restaurant_owners values (ip_username);
end //
delimiter ;

-- [2] add_employee()
-- -----------------------------------------------------------------------------
/* This stored procedure creates a new employee without any designated pilot or
worker roles.  A new employee must have a unique username unique tax identifier. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_employee;
delimiter //
create procedure add_employee (in ip_username varchar(40), in ip_first_name varchar(100),
	in ip_last_name varchar(100), in ip_address varchar(500), in ip_birthdate date,
    in ip_taxID varchar(40), in ip_hired date, in ip_employee_experience integer,
    in ip_salary integer)
sp_main: begin
    if ((ip_username in (select username from users)) or 
    (ip_taxID in (select taxID from employees)))
    then leave sp_main; end if;
    insert into users values (ip_username, ip_first_name, ip_last_name, ip_address, ip_birthdate);
    insert into employees values (ip_username, ip_taxID, ip_hired, ip_employee_experience, ip_salary);
end //
delimiter ;

-- [3] add_pilot_role()
-- -----------------------------------------------------------------------------
/* This stored procedure adds the pilot role to an existing employee.  The
employee/new pilot must have a unique license identifier. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_pilot_role;
delimiter //
create procedure add_pilot_role (in ip_username varchar(40), in ip_licenseID varchar(40),
	in ip_pilot_experience integer)
sp_main: begin
	if (ip_username not in (select username from employees) or 
    ip_licenseID in (select licenseID from pilots))
    then leave sp_main; end if;
    
    insert into pilots values (ip_username, ip_licenseID, ip_pilot_experience);
end //
delimiter ;

-- [4] add_worker_role()
-- -----------------------------------------------------------------------------
/* This stored procedure adds the worker role to an existing employee. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_worker_role;
delimiter //
create procedure add_worker_role (in ip_username varchar(40))
sp_main: begin
	if (ip_username not in (select username from employees))
    then leave sp_main; end if;
    
    insert into workers values (ip_username);
end //
delimiter ;

-- [5] add_ingredient()
-- -----------------------------------------------------------------------------
/* This stored procedure creates a new ingredient.  A new ingredient must have a
unique barcode. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_ingredient;
delimiter //
create procedure add_ingredient (in ip_barcode varchar(40), in ip_iname varchar(100),
	in ip_weight integer)
sp_main: begin
	if (ip_barcode in (select barcode from ingredients))
    then leave sp_main; end if;
	
    insert into ingredients values (ip_barcode, ip_iname, ip_weight);
end //
delimiter ;

-- [6] add_drone()
-- -----------------------------------------------------------------------------
/* This stored procedure creates a new drone.  A new drone must be assigned 
to a valid delivery service and must have a unique tag.  Also, it must be flown
by a valid pilot initially (i.e., pilot works for the same service), but the pilot
can switch the drone to working as part of a swarm later. And the drone's starting
location will always be the delivery service's home base by default. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_drone;
delimiter //
create procedure add_drone (in ip_id varchar(40), in ip_tag integer, in ip_fuel integer,
	in ip_capacity integer, in ip_sales integer, in ip_flown_by varchar(40))
sp_main: begin
	if ((ip_id in (select id from drones where tag = ip_tag)) or (ip_id not in (select id from delivery_services))
    or (ip_flown_by not in (select username from pilots)) or (ip_flown_by not in (select username from work_for where id = ip_id)))
    then leave sp_main; end if;
	
    insert into drones values (ip_id, ip_tag, ip_fuel, ip_capacity, ip_sales, ip_flown_by, null, null, (select home_base from delivery_services where id=ip_id));
end //
delimiter ;

-- [7] add_restaurant()
-- -----------------------------------------------------------------------------
/* This stored procedure creates a new restaurant.  A new restaurant must have a
unique (long) name and must exist at a valid location, and have a valid rating.
And a resturant is initially "independent" (i.e., no owner), but will be assigned
an owner later for funding purposes. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_restaurant;
delimiter //
create procedure add_restaurant (in ip_long_name varchar(40), in ip_rating integer,
	in ip_spent integer, in ip_location varchar(40))
sp_main: begin
	if ((ip_long_name in (select long_name from restaurants)) or (ip_location not in (select label from locations)) or (ip_rating < 1) or (ip_rating > 5))
    then leave sp_main; end if;
	
    insert into restaurants values (ip_long_name, ip_rating, ip_spent, ip_location, null);
end //
delimiter ;

-- [8] add_service()
-- -----------------------------------------------------------------------------
/* This stored procedure creates a new delivery service.  A new service must have
a unique identifier, along with a valid home base and manager. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_service;
delimiter //
create procedure add_service (in ip_id varchar(40), in ip_long_name varchar(100),
	in ip_home_base varchar(40), in ip_manager varchar(40))
sp_main: begin
	if ((ip_id in (select id from delivery_services)) or (ip_home_base not in (select label from locations)) or (ip_manager not in (select * from workers)) or (ip_manager in (select manager from delivery_services)))
    then leave sp_main; end if;
	
    insert into delivery_services values (ip_id, ip_long_name, ip_home_base, ip_manager);
end //
delimiter ;

-- [9] add_location()
-- -----------------------------------------------------------------------------
/* This stored procedure creates a new location that becomes a new valid drone
destination.  A new location must have a unique combination of coordinates.  We
could allow for "aliased locations", but this might cause more confusion that
it's worth for our relatively simple system. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_location;
delimiter //
create procedure add_location (in ip_label varchar(40), in ip_x_coord integer,
	in ip_y_coord integer, in ip_space integer)
sp_main: begin
	if ((ip_label in (select label from locations)) or (ip_x_coord in (select x_coord from locations where y_coord = ip_y_coord)))
    then leave sp_main; end if;
    
    insert into locations values (ip_label, ip_x_coord, ip_y_coord, ip_space);
end //
delimiter ;

-- [10] start_funding()
-- -----------------------------------------------------------------------------
/* This stored procedure opens a channel for a restaurant owner to provide funds
to a restaurant. If a different owner is already providing funds, then the current
owner is replaced with the new owner.  The owner and restaurant must be valid. */
-- -----------------------------------------------------------------------------
drop procedure if exists start_funding;
delimiter //
create procedure start_funding (in ip_owner varchar(40), in ip_long_name varchar(40))
sp_main: begin
	if ((ip_owner not in (select * from restaurant_owners)) or (ip_long_name not in (select long_name from restaurants)))
	then leave sp_main; end if;
    
    update restaurants set funded_by = ip_owner where long_name = ip_long_name;
end //
delimiter ;

-- [11] hire_employee()
-- -----------------------------------------------------------------------------
/* This stored procedure hires an employee to work for a delivery service.
Employees can be combinations of workers and pilots. If an employee is actively
controlling drones or serving as manager for a different service, then they are
not eligible to be hired.  Otherwise, the hiring is permitted. */
-- -----------------------------------------------------------------------------
drop procedure if exists hire_employee;
delimiter // 
create procedure hire_employee (in ip_username varchar(40), in ip_id varchar(40))
sp_main: begin
	if ((ip_username not in (select username from employees)) or (ip_id not in (select id from delivery_services)) 
	or (ip_username in (select manager from delivery_services where id != ip_id)) 
    or (ip_username in (select flown_by from drones where id != ip_id))
    or (ip_username in (select username from work_for where id = ip_id)))
    then leave sp_main; end if;
	
    insert into work_for values (ip_username, ip_id);
end //
delimiter ;

-- [12] fire_employee()
-- -----------------------------------------------------------------------------
/* This stored procedure fires an employee who is currently working for a delivery
service.  The only restrictions are that the employee must not be: [1] actively
controlling one or more drones; or, [2] serving as a manager for the service.
Otherwise, the firing is permitted. */
-- -----------------------------------------------------------------------------
drop procedure if exists fire_employee;
delimiter //
create procedure fire_employee (in ip_username varchar(40), in ip_id varchar(40))
sp_main: begin
	if ((ip_username not in (select username from work_for)) or (ip_username in (select manager from delivery_services)) 
    or (ip_username in (select flown_by from drones)))
    then leave sp_main; end if;
    
    delete from work_for where (username = ip_username and id = ip_id);
	-- ensure that the employee is currently working for the service
    -- ensure that the employee isn't an active manager
	-- ensure that the employee isn't controlling any drones
end //
delimiter ;

-- [13] manage_service()
-- -----------------------------------------------------------------------------
/* This stored procedure appoints an employee who is currently hired by a delivery
service as the new manager for that service.  The only restrictions are that: [1]
the employee must not be working for any other delivery service; and, [2] the
employee can't be flying drones at the time.  Otherwise, the appointment to manager
is permitted.  The current manager is simply replaced.  And the employee must be
granted the worker role if they don't have it already. */
-- -----------------------------------------------------------------------------
drop procedure if exists manage_service;
delimiter //
create procedure manage_service (in ip_username varchar(40), in ip_id varchar(40))
sp_main: begin
	if ((ip_username not in (select username from work_for where id = ip_id)) or (ip_username in (select flown_by from drones)) or
    ip_username in (select username from work_for where id != ip_id))
    then leave sp_main; end if;
    
    if (ip_username not in (select username from workers))
    then insert into workers values (ip_username); end if;
    
    update delivery_services set manager = ip_username where id = ip_id;
	-- ensure that the employee is currently working for the service
	-- ensure that the employee is not flying any drones
    -- ensure that the employee isn't working for any other services
    -- add the worker role if necessary
end //
delimiter ;

-- [14] takeover_drone()
-- -----------------------------------------------------------------------------
/* This stored procedure allows a valid pilot to take control of a lead drone owned
by the same delivery service, whether it's a "lone drone" or the leader of a swarm.
The current controller of the drone is simply relieved of those duties. And this
should only be executed if a "leader drone" is selected. */
-- -----------------------------------------------------------------------------
drop procedure if exists takeover_drone;
delimiter //
create procedure takeover_drone (in ip_username varchar(40), in ip_id varchar(40),
	in ip_tag integer)
sp_main: begin
	if ((ip_username not in (select username from work_for where id = ip_id)) or (ip_username not in (select username from pilots)) or
    ((select flown_by from drones where (id = ip_id and tag = ip_tag)) is null) or (ip_username in (select manager from delivery_services)))
    then leave sp_main; end if;
    
    update drones set flown_by = ip_username where id = ip_id and tag = ip_tag;
end //
delimiter ;

-- [15] join_swarm()
-- -----------------------------------------------------------------------------
/* This stored procedure takes a drone that is currently being directly controlled
by a pilot and has it join a swarm (i.e., group of drones) led by a different
directly controlled drone. A drone that is joining a swarm connot be leading a
different swarm at this time.  Also, the drones must be at the same location, but
they can be controlled by different pilots. */
-- -----------------------------------------------------------------------------
drop procedure if exists join_swarm;
delimiter //
create procedure join_swarm (in ip_id varchar(40), in ip_tag integer,
	in ip_swarm_leader_tag integer)
sp_main: begin
	if ((ip_tag = ip_swarm_leader_tag) or (ip_id not in (select id from drones where tag = ip_tag)) or 
    (ip_tag in (select tag from drones where (swarm_id = ip_id and swarm_tag = tag))) 
    or ((select flown_by from drones where (id = ip_id and tag = ip_swarm_leader_tag)) is null) or
    ((select hover from drones where id = ip_id and tag = ip_swarm_leader_tag) != (select hover from drones where id = ip_id and tag = ip_tag)))
    then leave sp_main; end if;
    
    update drones set flown_by = null, swarm_id = ip_id, swarm_tag = ip_swarm_leader_tag where (id = ip_id and tag = ip_tag);
end //
delimiter ;

-- [16] leave_swarm()
-- -----------------------------------------------------------------------------
/* This stored procedure takes a drone that is currently in a swarm and returns
it to being directly controlled by the same pilot who's controlling the swarm. */
-- -----------------------------------------------------------------------------
drop procedure if exists leave_swarm;
delimiter //
create procedure leave_swarm (in ip_id varchar(40), in ip_swarm_tag integer)
sp_main: begin
	if ((ip_swarm_tag not in (select tag from drones where id = ip_id)) or ((select flown_by from drones where (id = ip_id and tag = ip_swarm_tag)) is not null))
	then leave sp_main; end if;
    
    update drones set flown_by = (select flown_by from (select * from drones) as drone_table where (id = ip_id and tag = (select swarm_tag from (select * from drones) as drone_table2 where (id = ip_id and tag = ip_swarm_tag)))), swarm_tag = null, swarm_id = null
    where (id = ip_id and tag = ip_swarm_tag);
end //
delimiter ;

-- [17] load_drone()
-- -----------------------------------------------------------------------------
/* This stored procedure allows us to add some quantity of fixed-size packages of
a specific ingredient to a drone's payload so that we can sell them for some
specific price to other restaurants.  The drone can only be loaded if it's located
at its delivery service's home base, and the drone must have enough capacity to
carry the increased number of items.

The change/delta quantity value must be positive, and must be added to the quantity
of the ingredient already loaded onto the drone as applicable.  And if the ingredient
already exists on the drone, then the existing price must not be changed. */
-- -----------------------------------------------------------------------------
drop procedure if exists load_drone;
delimiter //
create procedure load_drone (in ip_id varchar(40), in ip_tag integer, in ip_barcode varchar(40),
	in ip_more_packages integer, in ip_price integer)
sp_main: begin
	if ((ip_tag not in (select tag from drones where id = ip_id)) or (ip_barcode not in (select barcode from ingredients)) or 
    ((select hover from drones where id = ip_id and tag = ip_tag) != (select home_base from delivery_services where id = ip_id)) or
    (ip_more_packages <= 0) or ((select capacity from drones where id = ip_id and tag = ip_tag) < 
    ((select sum(quantity) from payload where id = ip_id and tag = ip_tag) + ip_more_packages)))
    then leave sp_main; end if;
    
    if (ip_barcode in (select barcode from payload where id = ip_id and tag = ip_tag))
    then update payload set quantity = (quantity + ip_more_packages) where id = ip_id and tag = ip_tag and barcode = ip_barcode;
    else insert into payload values (ip_id, ip_tag, ip_barcode, ip_more_packages, ip_price); end if;
end //
delimiter ;

-- [18] refuel_drone()
-- -----------------------------------------------------------------------------
/* This stored procedure allows us to add more fuel to a drone. The drone can only
be refueled if it's located at the delivery service's home base. */
-- -----------------------------------------------------------------------------
drop procedure if exists refuel_drone;
delimiter //
create procedure refuel_drone (in ip_id varchar(40), in ip_tag integer, in ip_more_fuel integer)
sp_main: begin
	if ((ip_tag not in (select tag from drones where id = ip_id)) or 
    ((select hover from drones where id = ip_id and tag = ip_tag) != (select home_base from delivery_services where id = ip_id)))
    then leave sp_main; end if;
    
    update drones set fuel = fuel + ip_more_fuel where id = ip_id and tag = ip_tag;
	-- ensure that the drone being switched is valid and owned by the service
    -- ensure that the drone is located at the service home base
end //
delimiter ;

-- [19] fly_drone()
-- -----------------------------------------------------------------------------
/* This stored procedure allows us to move a single or swarm of drones to a new
location (i.e., destination). The main constraints on the drone(s) being able to
move to a new location are fuel and space.  A drone can only move to a destination
if it has enough fuel to reach the destination and still move from the destination
back to home base.  And a drone can only move to a destination if there's enough
space remaining at the destination.  For swarms, the flight directions will always
be given to the lead drone, but the swarm must always stay together. */
-- -----------------------------------------------------------------------------
drop function if exists fuel_required;
delimiter //
create function fuel_required (ip_departure varchar(40), ip_arrival varchar(40))
	returns integer reads sql data
begin
	if (ip_departure = ip_arrival) then return 0;
    else return (select 1 + truncate(sqrt(power(arrival.x_coord - departure.x_coord, 2) + power(arrival.y_coord - departure.y_coord, 2)), 0) as fuel
		from (select x_coord, y_coord from locations where label = ip_departure) as departure,
        (select x_coord, y_coord from locations where label = ip_arrival) as arrival);
	end if;
end //
delimiter ;

drop procedure if exists fly_drone;
delimiter //
create procedure fly_drone (in ip_id varchar(40), in ip_tag integer, in ip_destination varchar(40))
sp_main: begin
	if ((ip_tag not in (select tag from drones where id = ip_id)) or (ip_destination not in (select label from locations))
    or ((select hover from drones where id = ip_id and tag = ip_tag) = ip_destination) or
    ((fuel_required((select hover from drones where id = ip_id and tag = ip_tag), ip_destination) + fuel_required(ip_destination, 
    (select home_base from delivery_services where id = ip_id))) > 
    (select min(fuel) from drones where (id = ip_id and tag = ip_tag) or (swarm_id = ip_id and swarm_tag = ip_tag)))
    or (((select space from locations where label = ip_destination) - (select count(*) from drones where hover = ip_destination)) 
    < ((select count(*) from drones where swarm_id = ip_id and swarm_tag = ip_tag) + 1)))
    then leave sp_main; end if;
    
    update drones set fuel = (fuel - (fuel_required((select hover from (select * from drones) as drone_table where id = ip_id and tag = ip_tag), ip_destination)))
    where ((id = ip_id and tag = ip_tag) or (swarm_id = ip_id and swarm_tag = ip_tag));
    update drones set hover = ip_destination where ((id = ip_id and tag = ip_tag) or (swarm_id = ip_id and swarm_tag = ip_tag));
end //
delimiter ;

-- [20] purchase_ingredient()
-- -----------------------------------------------------------------------------
/* This stored procedure allows a restaurant to purchase ingredients from a drone
at its current location.  The drone must have the desired quantity of the ingredient
being purchased.  And the restaurant must have enough money to purchase the
ingredients.  If the transaction is otherwise valid, then the drone and restaurant
information must be changed appropriately.  Finally, we need to ensure that all
quantities in the payload table (post transaction) are greater than zero. */
-- -----------------------------------------------------------------------------
drop procedure if exists purchase_ingredient;
delimiter //
create procedure purchase_ingredient (in ip_long_name varchar(40), in ip_id varchar(40),
	in ip_tag integer, in ip_barcode varchar(40), in ip_quantity integer)
sp_main: begin
	if ((ip_long_name not in (select long_name from restaurants)) or (ip_tag not in (select tag from drones where id = ip_id)) or
    ((select location from restaurants where long_name = ip_long_name) != (select hover from drones where (id = ip_id and tag = ip_tag))) or 
    (ip_quantity > (select quantity from payload where (id = ip_id and tag = ip_tag and barcode = ip_barcode))))
    then leave sp_main; end if;
    
    update payload set quantity = (quantity - ip_quantity) where (id = ip_id and tag = ip_tag and barcode = ip_barcode);
    update restaurants set spent = (spent + (ip_quantity * (select price from payload where (id = ip_id and tag = ip_tag and barcode = ip_barcode))))
    where long_name = ip_long_name;
    update drones set sales = (sales + (ip_quantity * (select price from payload where (id = ip_id and tag = ip_tag and barcode = ip_barcode))))
    where (id = ip_id and tag = ip_tag);
    if ((select quantity from payload where (id = ip_id and tag = ip_tag and barcode = ip_barcode)) = 0)
    then delete from payload where quantity = 0; end if;
end //
delimiter ;

-- [21] remove_ingredient()
-- -----------------------------------------------------------------------------
/* This stored procedure removes an ingredient from the system.  The removal can
occur if, and only if, the ingredient is not being carried by any drones. */
-- -----------------------------------------------------------------------------
drop procedure if exists remove_ingredient;
delimiter //
create procedure remove_ingredient (in ip_barcode varchar(40))
sp_main: begin
	if ((ip_barcode not in (select barcode from ingredients)) or (ip_barcode in (select barcode from payload)))
    then leave sp_main; end if;
    
    delete from ingredients where barcode = ip_barcode;
end //
delimiter ;

-- [22] remove_drone()
-- -----------------------------------------------------------------------------
/* This stored procedure removes a drone from the system.  The removal can
occur if, and only if, the drone is not carrying any ingredients, and if it is
not leading a swarm. */
-- -----------------------------------------------------------------------------
drop procedure if exists remove_drone;
delimiter //
create procedure remove_drone (in ip_id varchar(40), in ip_tag integer)
sp_main: begin
	if ((ip_tag not in (select tag from drones where id = ip_id)) or (ip_tag in (select tag from payload where id = ip_id)) or
    (ip_tag in (select swarm_tag from drones where swarm_id = ip_id)))
    then leave sp_main; end if;
    
    delete from drones where (id = ip_id and tag = ip_tag);
end //
delimiter ;

-- [23] remove_pilot_role()
-- -----------------------------------------------------------------------------
/* This stored procedure removes a pilot from the system.  The removal can
occur if, and only if, the pilot is not controlling any drones.  Also, if the
pilot also has a worker role, then the worker information must be maintained;
otherwise, the pilot's information must be completely removed from the system. */
-- -----------------------------------------------------------------------------
drop procedure if exists remove_pilot_role;
delimiter //
create procedure remove_pilot_role (in ip_username varchar(40))
sp_main: begin
	if ((ip_username not in (select username from pilots)) or (ip_username in (select flown_by from drones)))
    then leave sp_main; end if;
    
    delete from pilots where username = ip_username;
    if (ip_username in (select username from workers))
    then leave sp_main;
    else delete from users where username = ip_username;
    end if;
end //
delimiter ;

-- [24] display_owner_view()
-- -----------------------------------------------------------------------------
/* This view displays information in the system from the perspective of an owner.
For each owner, it includes the owner's information, along with the number of
restaurants for which they provide funds and the number of different places where
those restaurants are located.  It also includes the highest and lowest ratings
for each of those restaurants, as well as the total amount of debt based on the
monies spent purchasing ingredients by all of those restaurants. And if an owner
doesn't fund any restaurants then display zeros for the highs, lows and debt. */
-- -----------------------------------------------------------------------------
create or replace view display_owner_view as
select restaurant_owners.username, first_name, last_name, address, count(long_name) as num_of_restaurants, count(distinct location) as num_of_locations, 
IFNull(max(rating), 0) as max_rating, IFNull(min(rating), 0) as min_rating, IFNull(sum(spent), 0) as total_spent
from restaurant_owners
join users on restaurant_owners.username = users.username
left outer join restaurants on restaurant_owners.username = funded_by group by username;

-- [25] display_employee_view()
-- -----------------------------------------------------------------------------
/* This view displays information in the system from the perspective of an employee.
For each employee, it includes the username, tax identifier, hiring date and
experience level, along with the license identifer and piloting experience (if
applicable), and a 'yes' or 'no' depending on the manager status of the employee. */
-- -----------------------------------------------------------------------------
create or replace view display_employee_view as
select employees.username, taxID, salary, hired, employees.experience as employee_experience,  ifnull(licenseID, 'n/a') , ifnull(pilots.experience, 'n/a') as successful_flights, 
CASE when (employees.username in (select manager from delivery_services)) then 'yes' else 'no' end as manager
from employees
left outer join
pilots on employees.username = pilots.username;

-- [26] display_pilot_view()
-- -----------------------------------------------------------------------------
/* This view displays information in the system from the perspective of a pilot.
For each pilot, it includes the username, licenseID and piloting experience, along
with the number of drones that they are controlling. */
-- -----------------------------------------------------------------------------
create or replace view display_pilot_view as
select username, licenseID, experience, (select count(*) from drones where ((flown_by = username) or ((swarm_id in (select id from drones where flown_by = username)) 
and swarm_tag in (select tag from drones where flown_by = username)))) as current_drones, (select count(distinct hover) from drones where 
((flown_by = username) or ((swarm_id in (select id from drones where flown_by = username)) and swarm_tag in 
(select tag from drones where flown_by = username)))) as num_locations from pilots;

-- [27] display_location_view()
-- -----------------------------------------------------------------------------
/* This view displays information in the system from the perspective of a location.
For each location, it includes the label, x- and y- coordinates, along with the
number of restaurants, delivery services and drones at that location. */
-- -----------------------------------------------------------------------------
create or replace view display_location_view as
select label, x_coord, y_coord, ifnull((select count(*) from restaurants where label = location group by location), 0) as num_restaurants,
ifnull((select count(*) from delivery_services where label = home_base group by home_base), 0) as num_delievery_services,
ifnull((select count(*) from drones where label = hover group by hover), 0) as num_drones 
from locations;

-- [28] display_ingredient_view()
-- -----------------------------------------------------------------------------
/* This view displays information in the system from the perspective of the ingredients.
For each ingredient that is being carried by at least one drone, it includes a list of
the various locations where it can be purchased, along with the total number of packages
that can be purchased and the lowest and highest prices at which the ingredient is being
sold at that location. */
-- -----------------------------------------------------------------------------
create or replace view display_ingredient_view as
select iname, hover, (select sum(quantity) from payload where (payload.barcode = ingredients.barcode 
and payload.id = drones.id and payload.tag = drones.tag)) as total_quantity, (select min(price) from payload where 
(payload.barcode = ingredients.barcode and payload.id = drones.id and payload.tag = drones.tag)) as min_price, (select max(price) 
from payload where (payload.barcode = ingredients.barcode and payload.id = drones.id and payload.tag = drones.tag)) 
as max_price from ingredients
join
payload on payload.barcode = ingredients.barcode
join
drones on (payload.id = drones.id and payload.tag = drones.tag) order by iname, hover;

-- [29] display_service_view()
-- -----------------------------------------------------------------------------
/* This view displays information in the system from the perspective of a delivery
service.  It includes the identifier, name, home base location and manager for the
service, along with the total sales from the drones.  It must also include the number
of unique ingredients along with the total cost and weight of those ingredients being
carried by the drones. */
-- -----------------------------------------------------------------------------
create or replace view display_service_view as
select delivery_services.*, (select sum(sales) from drones where drones.id = delivery_services.id group by id) as total_sales,
count(distinct payload.barcode) as num_different_ingredients, sum(quantity * price) as total_cost_of_products,
sum(quantity * weight) as total_weight_of_products from delivery_services
join
payload on delivery_services.id = payload.id
join
ingredients on payload.barcode = ingredients.barcode group by delivery_services.id;
