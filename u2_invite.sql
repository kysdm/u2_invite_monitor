/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 80027
 Source Host           : localhost:3306
 Source Schema         : u2_invite

 Target Server Type    : MySQL
 Target Server Version : 80027
 File Encoding         : 65001

 Date: 28/02/2022 23:16:50
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for u2_info
-- ----------------------------
DROP TABLE IF EXISTS `u2_info`;
CREATE TABLE `u2_info`  (
  `Self` int(0) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `Get_Time` datetime(0) NOT NULL COMMENT '数据获取的时间',
  `User_ID` int(0) NOT NULL COMMENT '用户UID',
  `User_Name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '用户昵称',
  `Join_Date` datetime(0) NOT NULL COMMENT '加入时间',
  `Last_Seen` datetime(0) NOT NULL COMMENT '上次登录时间',
  `Gender` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '性别',
  `User_Class` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '用户等级',
  `Uploaded` float NOT NULL COMMENT '虚拟上传量',
  `Downloaded` float NOT NULL COMMENT '虚拟下载量',
  `Raw_Uploaded` float NOT NULL COMMENT '实际上传量',
  `Raw_Downloaded` float NOT NULL COMMENT '实际下载量',
  `UCoin` int(0) NOT NULL COMMENT 'UC存量',
  `EXP` int(0) NOT NULL COMMENT '魔法经验',
  `Seeding_Time` int(0) NOT NULL COMMENT '做种时间',
  `Downloading_Time` int(0) NOT NULL COMMENT '下载时间',
  `Torrent_Comments` int(0) NOT NULL COMMENT '种子评论数量',
  `Forum_Posts` int(0) NOT NULL COMMENT '论坛评论数量',
  `Uploaded_Torrents_Quantity` int(0) NOT NULL COMMENT '上传种子数量',
  `Uploaded_Torrents_Size` int(0) NOT NULL COMMENT '上传种子体积',
  `Currently_Seeding_Quantity` int(0) NOT NULL COMMENT '做种种子数量',
  `Currently_Seeding_Size` int(0) NOT NULL COMMENT '做种种子体积',
  `Completed_Torrents_Quantity` int(0) NOT NULL COMMENT '完成种子数量',
  `Completed_Torrents_Size` int(0) NOT NULL COMMENT '完成种子体积',
  PRIMARY KEY (`Self`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for u2_user
-- ----------------------------
DROP TABLE IF EXISTS `u2_user`;
CREATE TABLE `u2_user`  (
  `id` int(0) NOT NULL COMMENT 'UID',
  `requirement` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '考核内容',
  `ctime` datetime(0) NULL DEFAULT NULL COMMENT '添加时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
