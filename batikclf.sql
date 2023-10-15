-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 15, 2023 at 05:14 PM
-- Server version: 10.4.20-MariaDB
-- PHP Version: 8.0.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `batikclf`
--

-- --------------------------------------------------------

--
-- Table structure for table `predictresult`
--

CREATE TABLE `predictresult` (
  `no` int(11) NOT NULL,
  `gambar` varchar(255) NOT NULL,
  `hasil` varchar(100) NOT NULL,
  `prob` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `predictresult`
--

INSERT INTO `predictresult` (`no`, `gambar`, `hasil`, `prob`) VALUES
(1, 'baru_0051,sekarjagad.jpg', 'Parang', 79.712),
(2, 'baru_0032,truntum.jpg', 'Truntum', 98.7927),
(3, 'Baru_0008,megamendung.jpg', 'Megamendung', 0.971973);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `predictresult`
--
ALTER TABLE `predictresult`
  ADD PRIMARY KEY (`no`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `predictresult`
--
ALTER TABLE `predictresult`
  MODIFY `no` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
