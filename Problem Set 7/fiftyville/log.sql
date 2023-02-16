-- Keep a log of any SQL queries you execute as you solve the mystery.

-- First Step is to identify crime reports on the day and location provide.

SELECT id, description
FROM crime_scene_reports
WHERE year = 2021 AND month = 7 AND day = 28 AND street = 'Humphrey Street';

-- Only 2 reports one of the CS50 Duck (theft) w/ 3 witnesses. The other littering.

--Review witness statments

SELECT name, transcript
FROM interviews
WHERE year = 2021
AND month = 7
AND day = 28;

-- Summary Witness reports from:
-- RUTH: Theif got in car within 10 minutes of the theft: Time range - 10:15am - 10:25 am
-- Eugene: Saw Theft early at the ATM on Leggett Street and saw the thief there withdrawing some money.
-- Raymond: Theif called accomplice when leave bakery, planned on taking the earliest flight out tomorrow (7/29/2021). accomplice purchased ticket.


-- Identify license plate of car

SELECT name
FROM people
WHERE license_plate IN (SELECT license_plate
FROM bakery_security_logs
WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute BETWEEN 15 AND 25 AND activity = 'exit'
ORDER BY minute);


-- Following suspects license plate exited during the time interval : Vanessa, Barry, Iman, Sofia, Luca, Diana, Kelsey, Bruce

-- Suspects: Vanessa, Barry, Iman, Sofia, Luca, Diana, Kelsey, Bruce



-- Review Individuals who made ATM withdrawals prior to the thief.

SELECT name FROM people
JOIN bank_accounts ON bank_accounts.person_id = people.id
JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number
WHERE year = 2021 AND month = 7 AND day = 28
AND atm_location = "Leggett Street"
AND transaction_type = "withdraw";

--Results name: Bruce, Diana, Brooke, Kenny, Iman, Luca, Taylor, Benista

-- Suspects Remaining: Bruce, Diana, Iman, Luca

-- Check Call Logs
-- First the name of caller
SELECT name FROM people
JOIN phone_calls ON people.phone_number = phone_calls.caller
WHERE year = 2021 AND month = 7 AND day = 28
AND duration <= 60;

--Results name: Sofia, Kelsey, Bruce, Kathryn, Kelsey, Taylor, Diana, Carina, Kenny, Benista,

-- Suspects:  Bruce, Diana,

-- Call Recievers
SELECT name FROM people
JOIN phone_calls ON people.phone_number = phone_calls.receiver
WHERE year = 2021 AND month = 7 AND day = 28
AND duration <= 60;

-- Results name: Jack, Larry, Robin, Luca, Melissa, James, Philip, Jacqueline, Doris
-- Accomplices: name: Jack, Larry, Robin, Luca, Melissa, James, Philip, Jacqueline, Doris

-- Flights on 7/29/2021 after thieft
SELECT id, destination_airport_id FROM flights
WHERE year = 2021 AND month = 7 AND day = 29
ORDER BY hour, minute LIMIT 1;

--results:
-- +----+------------------------+
-- | id | destination_airport_id |
-- +----+------------------------+
-- | 36 | 4                      |

-- Target flight id 36


-- Destination Airport Idnentification
SELECT full_name, city FROM airports
WHERE airports.id = 4;

-- Result: NEW YORK CITY

-- Identify Passenger from flight with from suspect list

SELECT name FROM people
JOIN passengers ON people.passport_number = passengers.passport_number
JOIN flights ON flights.id = passengers.flight_id
WHERE destination_airport_id = 4
AND year = 2021 AND month = 7 AND day = 29;

-- Result Name: Doris, Sofia, Bruce, Edward, Kelsey, Taylor, Kenny, Luca\

-- Suspect: Bruce
-- Theif Identified: BRUCE

-- Identify Accomplice
SELECT phone_number FROM people
WHERE name = "Bruce";

-- Bruces phone number:
-- +----------------+
-- |  phone_number  |
-- +----------------+
-- | (367) 555-5533 |
-- +----------------+

SELECT name FROM people
JOIN phone_calls ON people.phone_number = phone_calls.receiver
WHERE year = 2021 AND month = 7 AND day = 28
AND duration <= 60
AND phone_calls.caller = "(367) 555-5533";

-- Result
-- +-------+
-- | name  |
-- +-------+
-- | Robin |
-- +-------+

-- Accomplice Identified as ROBIN