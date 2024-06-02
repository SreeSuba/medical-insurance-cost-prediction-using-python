-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Apr 12, 2024 at 03:47 PM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `python_medical_insurance_cost_prediction`
--

-- --------------------------------------------------------

--
-- Table structure for table `drug_cost_details`
--

CREATE TABLE `drug_cost_details` (
  `id` int(100) NOT NULL,
  `hospital` varchar(100) NOT NULL,
  'hospital_code' VARCHAR( 100 ) NOT NULL ,
  `treatment_name` varchar(100) NOT NULL,
  `drug_name` varchar(100) NOT NULL,
  `drug_cost` varchar(100) NOT NULL,
  `place` varchar(100) NOT NULL,
   FOREIGN KEY ( 'hospital_code' ) REFERENCES 'hospital'('hospital_code' )
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `drug_cost_details`
--


-- --------------------------------------------------------

--
-- Table structure for table `examination_details`
--

CREATE TABLE `examination_details` (
  `id` int(100) NOT NULL,
  `hospital` varchar(100) NOT NULL,
  'hospital_code' VARCHAR( 100 ) NOT NULL ,
  `treatment_name` varchar(100) NOT NULL,
  `doctor_fees` varchar(100) NOT NULL,
  `nurse_fees` varchar(100) NOT NULL,
  `maintenance_fees` varchar(100) NOT NULL,
  `place` varchar(100) NOT NULL,
   FOREIGN KEY ( 'hospital_code' ) REFERENCES 'treatment_cost_details'('hospital_code' )

) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `examination_details`
--


-- --------------------------------------------------------

--
-- Table structure for table `hospital_details`
--

CREATE TABLE `hospital_details` (
  `id` int(100) NOT NULL,
  `hospital_name` varchar(100) NOT NULL,
  `area` varchar(100) NOT NULL,
  `dean` varchar(100) NOT NULL,
  `hospital_code` varchar(100) NOT NULL,
  `address` varchar(100) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `date` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `hospital_details`
--


-- --------------------------------------------------------

--
-- Table structure for table `treatment_cost_details`
--

CREATE TABLE 'treatment_cost_details' (
  'id' int(100) NOT NULL,
 'hospital' varchar(100) NOT NULL,
  'hospital_code' varchar(100) PRIMARY KEY,
  'treatment_name' varchar(100) NOT NULL,
  'treatment_cost' varchar(100) NOT NULL,
  'operation_cost' varchar(100) NOT NULL,
  'room_rent' varchar(100) NOT NULL,
  'lab_charge' varchar(100) NOT NULL,
  'place' varchar(100) NOT NULL,
  'category' varchar(100) NOT NULL
); ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `treatment_cost_details`
--


-- --------------------------------------------------------

--
-- Table structure for table `upload_data`
--

CREATE TABLE `upload_data` (
  `id` int(100) NOT NULL,
  `user` varchar(100) NOT NULL,
  `smoking` varchar(100) NOT NULL,
  `drinking` varchar(100) NOT NULL,
  `region` varchar(100) NOT NULL,
  `payment` varchar(100) NOT NULL,
  `filename` varchar(100) NOT NULL,
  `status` varchar(100) NOT NULL,
  `report` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `upload_data`
--


-- --------------------------------------------------------

--
-- Table structure for table `user_details`
--

CREATE TABLE `user_details` (
  `id` int(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  `contact` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `address` varchar(100) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `date` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `user_details`
--

