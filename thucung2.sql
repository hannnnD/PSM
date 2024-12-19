-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 19, 2024 at 11:58 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `thucung2`
--

-- --------------------------------------------------------

--
-- Table structure for table `customertbl`
--

CREATE TABLE `customertbl` (
  `CustID` int(11) NOT NULL,
  `CustName` varchar(50) DEFAULT NULL,
  `CustNumber` text DEFAULT NULL,
  `CustAddress` varchar(100) DEFAULT NULL,
  `CustRegisDate` text DEFAULT NULL,
  `CustNotes` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `customertbl`
--

INSERT INTO `customertbl` (`CustID`, `CustName`, `CustNumber`, `CustAddress`, `CustRegisDate`, `CustNotes`) VALUES
(1, 'Nguyễn Văn A', '0123456789', 'Hà Nội', '2024-11-01', 'Khách hàng thân thiết'),
(2, 'Trần Thị B', '0987654321', 'TP Hồ Chí Minh', '2024-10-20', 'Yêu cầu chăm sóc đặc biệt'),
(3, 'Lê Văn C', '0912345678', 'Đà Nẵng', '2024-09-15', ''),
(4, 'Phạm Thị D', '0934567890', 'Hải Phòng', '2024-08-30', 'Khách hàng mới'),
(5, 'Hoàng Văn E', '0976543210', 'Cần Thơ', '2024-07-25', 'Giới thiệu bởi khách khác'),
(6, 'Đặng Thị F', '0901234567', 'Huế', '2024-06-20', ''),
(7, 'Ngô Văn G', '0945678901', 'Quảng Ninh', '2024-05-15', ''),
(8, 'Vũ Thị H', '0923456789', 'Nha Trang', '2024-04-10', 'Khách hàng lâu năm'),
(9, 'Bùi Văn I', '0981234567', 'Vũng Tàu', '2024-03-05', ''),
(10, 'Đỗ Thị J', '0967890123', 'Biên Hòa', '2024-02-01', 'Đã từng sử dụng dịch vụ huấn luyện'),
(11, 'Nguyễn Thị K', '0919876543', 'Bình Dương', '2024-01-25', ''),
(12, 'Phạm Văn L', '0934567891', 'Long An', '2023-12-15', 'Thú cưng đặc biệt'),
(13, 'Trần Thị M', '0978901234', 'An Giang', '2023-11-30', ''),
(14, 'Lê Văn N', '0904567892', 'Đồng Nai', '2023-10-15', ''),
(15, 'Hoàng Thị O', '0987654321', 'Kiên Giang', '2023-09-05', 'Đăng ký theo nhóm'),
(16, 'Đặng Văn P', '0912345678', 'Bến Tre', '2023-08-25', ''),
(17, 'Ngô Thị Q', '0945678901', 'Sóc Trăng', '2023-07-15', ''),
(18, 'Vũ Văn R', '0909876543', 'Quảng Trị', '2023-06-10', ''),
(19, 'Bùi Thị S', '0981234567', 'Thanh Hóa', '2023-05-20', ''),
(20, 'Đỗ Văn T', '0934567890', 'Nghệ An', '2023-04-15', 'Khách VIP');

-- --------------------------------------------------------

--
-- Table structure for table `employeetbl`
--

CREATE TABLE `employeetbl` (
  `EmpID` int(11) NOT NULL,
  `EmpName` varchar(50) DEFAULT NULL,
  `EmpDOB` text DEFAULT NULL,
  `EmpGender` varchar(10) DEFAULT NULL,
  `EmpNumber` int(11) DEFAULT NULL,
  `EmpAddress` varchar(100) DEFAULT NULL,
  `EmpStartDate` text DEFAULT NULL,
  `EmpSalary` int(11) DEFAULT NULL,
  `EmpWorkShift` varchar(20) DEFAULT NULL,
  `EmpStatus` varchar(20) DEFAULT NULL,
  `EmpNotes` varchar(100) DEFAULT NULL,
  `EmpRole` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `employeetbl`
--

INSERT INTO `employeetbl` (`EmpID`, `EmpName`, `EmpDOB`, `EmpGender`, `EmpNumber`, `EmpAddress`, `EmpStartDate`, `EmpSalary`, `EmpWorkShift`, `EmpStatus`, `EmpNotes`, `EmpRole`) VALUES
(1, 'Nguyễn Anh', '10/4/2023', 'Nam', 1312, 'DC1', '11/23/2024', 150000000, 'Ca 1, 2', 'Làm việc', 'none', 'Quản lý'),
(2, 'Nguyễn Tú', '11/28/2001', 'Nam', 123456789, 'DC1', '11/28/2024', 1500000, 'Ca 1, 2', 'Làm việc', 'none', 'Cashier');

-- --------------------------------------------------------

--
-- Table structure for table `invoicedetailtbl`
--

CREATE TABLE `invoicedetailtbl` (
  `InvoiceDetailID` int(11) NOT NULL,
  `InvoiceID` int(11) DEFAULT NULL,
  `ServiceID` int(11) DEFAULT NULL,
  `SQuantity` int(11) DEFAULT NULL,
  `SPrice` decimal(10,2) DEFAULT NULL,
  `TotalAmt` decimal(10,2) DEFAULT NULL,
  `idDate` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `invoicedetailtbl`
--

INSERT INTO `invoicedetailtbl` (`InvoiceDetailID`, `InvoiceID`, `ServiceID`, `SQuantity`, `SPrice`, `TotalAmt`, `idDate`) VALUES
(73, 1, 1, 1, 150000.00, 150000.00, '12/1/2024'),
(74, 2, 1, 1, 150000.00, 150000.00, '11/30/2024'),
(75, 2, 2, 1, 200000.00, 200000.00, '11/30/2024'),
(76, 2, 3, 1, 300000.00, 300000.00, '11/30/2024'),
(77, 2, 4, 1, 250000.00, 250000.00, '11/30/2024'),
(78, 3, 1, 1, 150000.00, 150000.00, '12/2/2024'),
(79, 3, 3, 1, 300000.00, 300000.00, '12/2/2024'),
(80, 3, 8, 2, 100000.00, 200000.00, '12/2/2024'),
(81, 4, 2, 1, 200000.00, 200000.00, '12/2/2024'),
(82, 4, 3, 1, 300000.00, 300000.00, '12/2/2024'),
(83, 5, 4, 1, 250000.00, 250000.00, '12/12/2024'),
(84, 5, 3, 1, 300000.00, 300000.00, '12/12/2024'),
(85, 5, 2, 1, 200000.00, 200000.00, '12/12/2024'),
(86, 5, 1, 1, 150000.00, 150000.00, '12/12/2024'),
(87, 6, 1, 1, 150000.00, 150000.00, '18/12/2024'),
(88, 7, 1, 1, 150000.00, 150000.00, '19/12/2024');

-- --------------------------------------------------------

--
-- Table structure for table `invoicetbl`
--

CREATE TABLE `invoicetbl` (
  `InvoiceID` int(11) NOT NULL,
  `InvoiceDate` text DEFAULT NULL,
  `CustID` int(11) DEFAULT NULL,
  `EmpID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `invoicetbl`
--

INSERT INTO `invoicetbl` (`InvoiceID`, `InvoiceDate`, `CustID`, `EmpID`) VALUES
(1, '12/1/2024', 1, 1),
(2, '11/30/2024', 1, 1),
(3, '12/2/2024', 5, 1),
(4, '12/2/2024', 3, 1),
(5, '12/12/2024', 2, 1),
(6, '18/12/2024', 1, 1),
(7, '19/12/2024', 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `petcareinvoicedetailtbl`
--

CREATE TABLE `petcareinvoicedetailtbl` (
  `PIVID` int(11) NOT NULL,
  `PetCareID` int(11) DEFAULT NULL,
  `TotalDays` int(11) DEFAULT NULL,
  `TotalAmt` decimal(10,2) DEFAULT NULL,
  `StartDate` decimal(10,0) NOT NULL,
  `EndDate` decimal(10,0) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `petcaretbl`
--

CREATE TABLE `petcaretbl` (
  `PetCareID` int(11) NOT NULL,
  `PetName` varchar(50) DEFAULT NULL,
  `PetBreed` varchar(50) DEFAULT NULL,
  `PetDOB` text DEFAULT NULL,
  `PetType` varchar(50) DEFAULT NULL,
  `StartDate` text DEFAULT NULL,
  `PetRoomID` int(11) DEFAULT NULL,
  `CustID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `petroomtbl`
--

CREATE TABLE `petroomtbl` (
  `PetRoomID` int(11) NOT NULL,
  `RName` varchar(50) DEFAULT NULL,
  `RStatus` enum('Trống','Đủ') DEFAULT NULL,
  `RType` text DEFAULT NULL,
  `RPrice` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `petroomtbl`
--

INSERT INTO `petroomtbl` (`PetRoomID`, `RName`, `RStatus`, `RType`, `RPrice`) VALUES
(1, 'Phòng A1', 'Trống', 'Chim', 200),
(2, 'Phòng A2', 'Trống', 'Chim', 200),
(3, 'Phòng B1', 'Trống', 'Thú', 300),
(4, 'Phòng B2', 'Trống', 'Thú', 300),
(5, 'Phòng C1', 'Trống', 'Khác', 250),
(6, 'Phòng C2', 'Trống', 'Chim', 200),
(7, 'Phòng D1', 'Trống', 'Thú', 300),
(8, 'Phòng D2', 'Trống', 'Khác', 250),
(9, 'Phòng E1', 'Trống', 'Thú', 300),
(10, 'Phòng E2', 'Trống', 'Chim', 200);

-- --------------------------------------------------------

--
-- Table structure for table `servicetbl`
--

CREATE TABLE `servicetbl` (
  `ServiceID` int(11) NOT NULL,
  `SName` varchar(50) DEFAULT NULL,
  `SCategories` varchar(50) DEFAULT NULL,
  `SQuantity` int(11) DEFAULT NULL,
  `SPrice` decimal(10,2) DEFAULT NULL,
  `SNotes` varchar(100) DEFAULT NULL,
  `SSupplier` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `servicetbl`
--

INSERT INTO `servicetbl` (`ServiceID`, `SName`, `SCategories`, `SQuantity`, `SPrice`, `SNotes`, `SSupplier`) VALUES
(1, 'Dịch vụ tắm rửa', 'Vệ sinh', 93, 150000.00, 'Dịch vụ vệ sinh cơ bản', NULL),
(2, 'Dịch vụ cắt tỉa', 'Làm đẹp', 46, 200000.00, 'Cắt tỉa lông chuyên nghiệp', NULL),
(3, 'Dịch vụ tiêm ngừa', 'Y tế', 195, 300000.00, 'Tiêm phòng định kỳ', NULL),
(4, 'Dịch vụ khám tổng quát', 'Y tế', 147, 250000.00, 'Khám sức khỏe định kỳ', NULL),
(5, 'Dịch vụ huấn luyện', 'Đào tạo', 30, 500000.00, 'Huấn luyện cơ bản', NULL),
(6, 'Dịch vụ trông giữ', 'Trông giữ', 50, 400000.00, 'Trông giữ thú cưng 1 ngày', NULL),
(7, 'Dịch vụ chải lông', 'Vệ sinh', 70, 120000.00, 'Chải lông sạch sẽ', NULL),
(8, 'Dịch vụ tư vấn', 'Tư vấn', 28, 100000.00, 'Tư vấn chăm sóc thú cưng', NULL),
(9, 'Dịch vụ vận chuyển', 'Vận chuyển', 20, 350000.00, 'Vận chuyển thú cưng an toàn', NULL),
(10, 'Dịch vụ điều trị', 'Y tế', 50, 450000.00, 'Điều trị bệnh cho thú cưng', NULL),
(11, 'Dịch vụ massage', 'Làm đẹp', 20, 300000.00, 'Massage thư giãn', NULL),
(12, 'Dịch vụ làm móng', 'Làm đẹp', 50, 150000.00, 'Dịch vụ làm móng đẹp', NULL),
(13, 'Dịch vụ lưu trú', 'Trông giữ', 30, 600000.00, 'Lưu trú dài hạn', NULL),
(14, 'Dịch vụ phẫu thuật', 'Y tế', 10, 5000000.00, 'Phẫu thuật thú y', NULL),
(15, 'Dịch vụ tẩy giun', 'Y tế', 150, 100000.00, 'Tẩy giun định kỳ', NULL),
(16, 'Dịch vụ nhuộm lông', 'Làm đẹp', 20, 800000.00, 'Nhuộm lông nghệ thuật', NULL),
(17, 'Dịch vụ xoa bóp cơ', 'Y tế', 25, 250000.00, 'Xoa bóp cơ cho thú cưng', NULL),
(18, 'Dịch vụ kiểm tra răng miệng', 'Y tế', 100, 200000.00, 'Kiểm tra và vệ sinh răng miệng', NULL),
(19, 'Dịch vụ xét nghiệm máu', 'Y tế', 40, 400000.00, 'Xét nghiệm máu định kỳ', NULL),
(20, 'Dịch vụ chăm sóc sinh sản', 'Y tế', 30, 700000.00, 'Chăm sóc thú cưng sau sinh', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `stockintbl`
--

CREATE TABLE `stockintbl` (
  `StockInID` int(11) NOT NULL,
  `SupplierID` int(11) NOT NULL,
  `ServiceID` int(11) NOT NULL,
  `Quantity` int(11) NOT NULL,
  `Price` decimal(10,2) NOT NULL,
  `DiscountedPrice` decimal(10,2) DEFAULT NULL,
  `TotalAmt` decimal(10,2) DEFAULT NULL,
  `StockInDate` text NOT NULL,
  `Notes` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `stockintbl`
--

INSERT INTO `stockintbl` (`StockInID`, `SupplierID`, `ServiceID`, `Quantity`, `Price`, `DiscountedPrice`, `TotalAmt`, `StockInDate`, `Notes`) VALUES
(1, 1, 2, 100, 50.00, 0.00, 5000.00, '2024-12-13', 'Nhập hàng tháng 12'),
(2, 1, 16, 10, 100000.00, 10000.00, 990000.00, '2024-12-13', 'no');

-- --------------------------------------------------------

--
-- Table structure for table `suppliertbl`
--

CREATE TABLE `suppliertbl` (
  `SupplierID` int(11) NOT NULL,
  `SupplierName` varchar(50) NOT NULL,
  `SupplierContact` text DEFAULT NULL,
  `SupplierAddress` varchar(100) DEFAULT NULL,
  `SupplierEmail` varchar(100) DEFAULT NULL,
  `SupplierNotes` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `suppliertbl`
--

INSERT INTO `suppliertbl` (`SupplierID`, `SupplierName`, `SupplierContact`, `SupplierAddress`, `SupplierEmail`, `SupplierNotes`) VALUES
(1, 'Công ty ABC', '0123456789', '123 Đường ABC, TP.HCM', NULL, 'Cung cấp dịch vụ thú y'),
(2, 'Công ty cổ phần ABC', '0987654321', 'Láng, Hòa Lạc, Hà Nội', 'ctycpabc123@gmail.com', 'Cung cấp dịch vụ nhà');

-- --------------------------------------------------------

--
-- Table structure for table `usertbl`
--

CREATE TABLE `usertbl` (
  `UserID` int(11) NOT NULL,
  `UserName` varchar(50) DEFAULT NULL,
  `Password` varchar(50) DEFAULT NULL,
  `Role` varchar(50) DEFAULT NULL,
  `EmpID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `usertbl`
--

INSERT INTO `usertbl` (`UserID`, `UserName`, `Password`, `Role`, `EmpID`) VALUES
(1, 'admin', '123', 'admin', 1),
(3, 'buadi', '123', 'Cashier', 2),
(4, 'NV1', '123', 'Cashier', 3),
(5, 'CS2', 'cs2', 'Cashier', 4);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `customertbl`
--
ALTER TABLE `customertbl`
  ADD PRIMARY KEY (`CustID`);

--
-- Indexes for table `employeetbl`
--
ALTER TABLE `employeetbl`
  ADD PRIMARY KEY (`EmpID`);

--
-- Indexes for table `invoicedetailtbl`
--
ALTER TABLE `invoicedetailtbl`
  ADD PRIMARY KEY (`InvoiceDetailID`),
  ADD KEY `InvoiceID` (`InvoiceID`),
  ADD KEY `ServiceID` (`ServiceID`);

--
-- Indexes for table `invoicetbl`
--
ALTER TABLE `invoicetbl`
  ADD PRIMARY KEY (`InvoiceID`),
  ADD KEY `CustID` (`CustID`),
  ADD KEY `EmpID` (`EmpID`);

--
-- Indexes for table `petcareinvoicedetailtbl`
--
ALTER TABLE `petcareinvoicedetailtbl`
  ADD PRIMARY KEY (`PIVID`),
  ADD KEY `PetCareID` (`PetCareID`);

--
-- Indexes for table `petcaretbl`
--
ALTER TABLE `petcaretbl`
  ADD PRIMARY KEY (`PetCareID`),
  ADD KEY `PetRoomID` (`PetRoomID`),
  ADD KEY `CustID` (`CustID`);

--
-- Indexes for table `petroomtbl`
--
ALTER TABLE `petroomtbl`
  ADD PRIMARY KEY (`PetRoomID`);

--
-- Indexes for table `servicetbl`
--
ALTER TABLE `servicetbl`
  ADD PRIMARY KEY (`ServiceID`);

--
-- Indexes for table `stockintbl`
--
ALTER TABLE `stockintbl`
  ADD PRIMARY KEY (`StockInID`),
  ADD KEY `SupplierID` (`SupplierID`),
  ADD KEY `ServiceID` (`ServiceID`);

--
-- Indexes for table `suppliertbl`
--
ALTER TABLE `suppliertbl`
  ADD PRIMARY KEY (`SupplierID`);

--
-- Indexes for table `usertbl`
--
ALTER TABLE `usertbl`
  ADD PRIMARY KEY (`UserID`),
  ADD KEY `EmpID` (`EmpID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `invoicedetailtbl`
--
ALTER TABLE `invoicedetailtbl`
  MODIFY `InvoiceDetailID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=89;

--
-- AUTO_INCREMENT for table `stockintbl`
--
ALTER TABLE `stockintbl`
  MODIFY `StockInID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `suppliertbl`
--
ALTER TABLE `suppliertbl`
  MODIFY `SupplierID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `usertbl`
--
ALTER TABLE `usertbl`
  MODIFY `UserID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `invoicedetailtbl`
--
ALTER TABLE `invoicedetailtbl`
  ADD CONSTRAINT `FK_ServiceID` FOREIGN KEY (`ServiceID`) REFERENCES `servicetbl` (`ServiceID`) ON DELETE SET NULL,
  ADD CONSTRAINT `invoicedetailtbl_ibfk_1` FOREIGN KEY (`InvoiceID`) REFERENCES `invoicetbl` (`InvoiceID`),
  ADD CONSTRAINT `invoicedetailtbl_ibfk_2` FOREIGN KEY (`ServiceID`) REFERENCES `servicetbl` (`ServiceID`);

--
-- Constraints for table `invoicetbl`
--
ALTER TABLE `invoicetbl`
  ADD CONSTRAINT `FK_CustID_InvoiceTbl` FOREIGN KEY (`CustID`) REFERENCES `customertbl` (`CustID`) ON DELETE SET NULL,
  ADD CONSTRAINT `FK_EmpID_InvoiceTbl` FOREIGN KEY (`EmpID`) REFERENCES `employeetbl` (`EmpID`) ON DELETE SET NULL,
  ADD CONSTRAINT `invoicetbl_ibfk_2` FOREIGN KEY (`EmpID`) REFERENCES `employeetbl` (`EmpID`);

--
-- Constraints for table `petcareinvoicedetailtbl`
--
ALTER TABLE `petcareinvoicedetailtbl`
  ADD CONSTRAINT `FK_PetCareID` FOREIGN KEY (`PetCareID`) REFERENCES `petcaretbl` (`PetCareID`) ON DELETE SET NULL,
  ADD CONSTRAINT `petcareinvoicedetailtbl_ibfk_2` FOREIGN KEY (`PetCareID`) REFERENCES `petcaretbl` (`PetCareID`);

--
-- Constraints for table `petcaretbl`
--
ALTER TABLE `petcaretbl`
  ADD CONSTRAINT `FK_CustID` FOREIGN KEY (`CustID`) REFERENCES `customertbl` (`CustID`) ON DELETE SET NULL,
  ADD CONSTRAINT `FK_PetRoomID` FOREIGN KEY (`PetRoomID`) REFERENCES `petroomtbl` (`PetRoomID`) ON DELETE SET NULL,
  ADD CONSTRAINT `petcaretbl_ibfk_1` FOREIGN KEY (`PetRoomID`) REFERENCES `petroomtbl` (`PetRoomID`),
  ADD CONSTRAINT `petcaretbl_ibfk_2` FOREIGN KEY (`CustID`) REFERENCES `customertbl` (`CustID`);

--
-- Constraints for table `stockintbl`
--
ALTER TABLE `stockintbl`
  ADD CONSTRAINT `stockintbl_ibfk_1` FOREIGN KEY (`SupplierID`) REFERENCES `suppliertbl` (`SupplierID`) ON DELETE CASCADE,
  ADD CONSTRAINT `stockintbl_ibfk_2` FOREIGN KEY (`ServiceID`) REFERENCES `servicetbl` (`ServiceID`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
