-- Team Members: Julie Anzaroot and Margaret Barnes
-- Project Title: Neighborhood Lending Library
-- Group 41
-- DML file for CRUD operations


---- READ Queries ----

-- Select all users
SELECT
  userID,
  firstName as 'First Name',
  lastName as 'Last Name',
  email as Email,
  phone as 'Phone Number'
FROM Users;


-- Select all resources
SELECT
  r.resourceID,
  r.resourceName as Name,
  r.resourceDescription as Description,
  u.firstName as 'Owner First Name',
  u.lastName as 'Owner Last Name'
FROM Resources r
JOIN Users u on r.userID = u.userID ;


-- Select all loans
SELECT
  l.loanID,
  l.startDate as 'Start Date',
  l.dueDate as 'Due Date',
  r.resourceName as 'Resource Name',
  u.firstName as 'Lender First Name',
  u.lasttName as 'Lender Last Name'
FROM Loans l
JOIN Users u on l.userID = u.userID
JOIN Resources r on l.resourceID = r.resourceID;


-- Select all locations
SELECT
  locationID,
  locationName,
  locationDescription
FROM Locations;


-- Select all ResourceLocations
SELECT
  rl.ResourceLocationsID,
  r.resourceName,
  l.locationName
FROM ResourceLocations rl
JOIN Resources r on rl.resourceID = r.resourceID
JOIN Locations l on rl.locationID = l.locationID;


---- CREATE Queries ----

-- Add a user
INSERT INTO Users (firstName, lastName, email, phone)
   VALUES (@firstName, @lastName, @email, @phone);


-- Add a resource
INSERT INTO Resources (userID, resourceName, resourceDescription)
VALUES(
  userID = (SELECT userID FROM Users WHERE userID = @userID),
  resourceName = @resourceName,
  resourceDescription = @resourceDescription
);


-- Add a location
INSERT INTO Locations (locationName, locationDescription)
   VALUES(@locationName, @locationDescription);


-- Add a ResourceLocation (M:M)
INSERT INTO ResourceLocations (resourceID, locationID)
VALUES(
  (SELECT resourceID FROM Resources WHERE resourceID = @resourceID),
  (SELECT locationID FROM Locations WHERE locationID = @locationID)
);


-- Add a loan
INSERT INTO Loans (startDate, dueDate, returnedDate, userID, resourceID)
   VALUES(
     @startDate,
     @dueDate,
     @returnedDate,
     (SELECT userID FROM Users WHERE userID = @userID),
     (SELECT resourceID FROM Resources WHERE resourceID = @resourceID)
   );


---- DELETE Queries ----

-- Delete a ResourceLocation (M:M)
DELETE FROM ResourceLocations
WHERE
 resourceID =  (SELECT resourceID FROM Resources WHERE resourceDescription = @resourceDescription)
 AND locationID =  (SELECT locationID FROM Locations WHERE locationName = @locationName);


-- Delete a Resource
DELETE FROM Resources
  WHERE resourceID = @resourceID


-- Delete a User
DELETE FROM Users
  WHERE userID = @userID


-- Delete a Loan
DELETE FROM Loans
  WHERE loanID = @loanID


-- Delete a Loaction
DELETE FROM Locations
  WHERE LoactionID = @locationID



---- UPDATE Queries ----
  
-- Update a Resource Description
UPDATE Resources
SET resourceDescription = @resourceDescription
WHERE resourceID = @resourceID


-- Update a ResourceLocation's locationID (M:M)
UPDATE ResourceLocations
SET
locationID = (SELECT locationID FROM Locations WHERE locationID = @locationID)
WHERE
 ResourceLocationsID =   @ResourceLocationsID;





