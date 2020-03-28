/*
 Navicat Premium Data Transfer

 Source Server         : benji
 Source Server Type    : MySQL
 Source Server Version : 50727
 Source Host           : localhost:3306
 Source Schema         : online_lassroom

 Target Server Type    : MySQL
 Target Server Version : 50727
 File Encoding         : 65001

 Date: 28/03/2020 16:43:44
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for accounts
-- ----------------------------
DROP TABLE IF EXISTS `accounts`;
CREATE TABLE `accounts`  (
  `aid` int(11) NOT NULL AUTO_INCREMENT COMMENT '用户id',
  `nickname` char(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '昵称',
  `username` char(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '账号',
  `pswd` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '密码',
  `status` tinyint(4) DEFAULT 0 COMMENT '身份状态',
  `info` text CHARACTER SET utf8 COLLATE utf8_general_ci COMMENT '一些额外的信息',
  `create_at` datetime(0) DEFAULT CURRENT_TIMESTAMP,
  `admin_id` int(11) DEFAULT NULL COMMENT '操作者员工id',
  `open_at` datetime(0) DEFAULT NULL COMMENT '操作时间',
  PRIMARY KEY (`aid`) USING BTREE,
  UNIQUE INDEX `nickname`(`nickname`) USING BTREE,
  UNIQUE INDEX `username`(`username`) USING BTREE,
  INDEX `admin_`(`admin_id`) USING BTREE,
  CONSTRAINT `admin_` FOREIGN KEY (`admin_id`) REFERENCES `admins_user` (`aid`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 10029 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of accounts
-- ----------------------------
INSERT INTO `accounts` VALUES (10000, '123', '123', '123', 0, NULL, '2020-03-01 00:23:18', NULL, NULL);
INSERT INTO `accounts` VALUES (10001, '456', '456', '456', 0, NULL, '2020-03-05 02:45:16', NULL, NULL);
INSERT INTO `accounts` VALUES (10003, '999', '999', 'pbkdf2:sha256:150000$IwLCGbai$046fd0ce75b8a64b17a4fd969df46f870300c68b6276c54429ce43693c97dd14', 2, NULL, '2020-03-06 00:23:01', NULL, NULL);
INSERT INTO `accounts` VALUES (10004, '100', '100', 'pbkdf2:sha256:150000$FSBXHU81$7bf638d7bb53d65fa843c5555eab556d3864e5d14faaa18c5b7657af90bab5d0', 2, NULL, '2020-03-08 00:23:06', NULL, NULL);
INSERT INTO `accounts` VALUES (10005, '101', '101', 'pbkdf2:sha256:150000$SXnc8fRi$31fbaf65f8da6e12eacc896e215857d5d19d76638c69266419a22a4dff920427', 2, '111111111111', '2020-03-09 08:29:10', NULL, NULL);
INSERT INTO `accounts` VALUES (10006, '102', '102', 'pbkdf2:sha256:150000$tthYxWzc$a3504ed1ac29a9e1a7e150c58e303c6a906327243817820670b4e7ef2add8854', 1, '102账号的up信息', '2020-03-14 16:06:24', NULL, NULL);
INSERT INTO `accounts` VALUES (10008, '学生账号', '103', 'pbkdf2:sha256:150000$RNbVND8F$3c50dc290a41a3046cd4b07fae1647e0eb4ac6cd5c608328970c8af7b32910c3', 2, '', '2020-03-15 23:37:48', NULL, NULL);
INSERT INTO `accounts` VALUES (10009, '学生账号1', '104', 'pbkdf2:sha256:150000$lSGO2jcp$c2983591cec0ba8661857c42f615e72607b382d9a85959750f623fac739e99be', 2, '', '2020-03-15 23:37:48', NULL, NULL);
INSERT INTO `accounts` VALUES (10011, '学生账号2', '105', 'pbkdf2:sha256:150000$JPz1SWox$50cc33aae142bfe0462d92cd41821f112ca82ffe31092d68345ae20f703cffc3', 2, '', '2020-03-15 23:37:48', NULL, NULL);
INSERT INTO `accounts` VALUES (10012, '学生账号3', '106', 'pbkdf2:sha256:150000$SRpCb12K$417e71a159e0d02b1eb1b353df6db942a77567fa2aa795ed13fb657d1107aec8', 10, '', '2020-03-15 23:37:48', 1, '2020-03-28 01:38:30');
INSERT INTO `accounts` VALUES (10014, '老师账号1', '107', 'pbkdf2:sha256:150000$AhX7K06K$a718b223660bc03f8e649587207458e242e6375588e83010293deef111a04e14', 2, '', '2020-03-15 23:42:33', 1, '2020-03-28 01:49:53');
INSERT INTO `accounts` VALUES (10015, '老师账号2', '108', 'pbkdf2:sha256:150000$BTNlElpd$d0961d0355c31084f06404257261eb20686e3af65c07afcc3bce442c1a6043f7', 1, '', '2020-03-15 23:42:33', NULL, NULL);
INSERT INTO `accounts` VALUES (10016, '老师账号3', '109', 'pbkdf2:sha256:150000$3Z8cuY6Q$45ec699311da755235ca6a458914204a0006d98239baef92c9010223733c6bdb', 1, '', '2020-03-15 23:42:33', NULL, NULL);
INSERT INTO `accounts` VALUES (10017, '老师账号4', '110', 'pbkdf2:sha256:150000$FFYmU0QQ$57c5d863d11484eae5071a5a6f9148da67b728bbb8ab3f189d87cfa68a3b3cf1', 1, '', '2020-03-15 23:42:33', NULL, NULL);
INSERT INTO `accounts` VALUES (10019, '老师账号5', '111', 'pbkdf2:sha256:150000$lcSYOjE1$9f2ed0639a044c381622b9606beab28fa9b6c497bb46c1a22a591167ff90b128', 1, NULL, '2020-03-18 17:37:15', NULL, NULL);
INSERT INTO `accounts` VALUES (10020, '老师账号', '112', 'pbkdf2:sha256:150000$6imiEevT$7c832225f0765db6c5aae0ecac83dd4086ca1f81b7348ec2522e1f0d9916a32a', 1, NULL, '2020-03-18 17:37:15', NULL, NULL);
INSERT INTO `accounts` VALUES (10021, '老师账号6', '113', 'pbkdf2:sha256:150000$xZnYFLs5$886a6df0bc54c2a26980c8bfbdb0052b0e037cccdf3663fa115bfc1ee0d3c4f4', 1, NULL, '2020-03-18 17:37:15', NULL, NULL);
INSERT INTO `accounts` VALUES (10022, '老师账号7', '114', 'pbkdf2:sha256:150000$vSqLDHMc$c55a7931474fe5928c0ce83249aac5ee73d9a52aaa2805836a891cf3104eeb6c', 1, NULL, '2020-03-18 17:37:15', NULL, NULL);
INSERT INTO `accounts` VALUES (10023, '老师账号8', '115', 'pbkdf2:sha256:150000$OG8Rhp60$a9cf54bf5c4fb46f17965b1dcd67f5ab30c13081e1ae57104a64d2e0ffbdc5ea', 1, NULL, '2020-03-18 17:37:15', NULL, NULL);
INSERT INTO `accounts` VALUES (10024, '老师账号9', '116', 'pbkdf2:sha256:150000$UXkFMSoq$3f37d7b145ced04cab28217b088602d7cf69bc53a72d8e6db45e54a93638c44a', 1, NULL, '2020-03-18 17:37:15', NULL, NULL);
INSERT INTO `accounts` VALUES (10025, '老师账号10', '117', 'pbkdf2:sha256:150000$MsY6yyA3$583b7945da3c9478889659597fb4c0112b08a498b9efdb257b7311c988e524ff', 1, NULL, '2020-03-18 17:37:15', NULL, NULL);
INSERT INTO `accounts` VALUES (10026, '老师账号11', '118', 'pbkdf2:sha256:150000$5Kx9lsat$195bff2a01f43a6fb1e496c7c6aa6ca032ed5d1f79c0022bf1eee558d714eb9f', 1, NULL, '2020-03-18 17:37:15', NULL, NULL);
INSERT INTO `accounts` VALUES (10027, '老师账号12', '119', 'pbkdf2:sha256:150000$IZJrViC0$01dfd755513940166be829b0145f89f51e7840a2a3732479d0c372536a373212', 1, NULL, '2020-03-18 17:37:15', NULL, NULL);
INSERT INTO `accounts` VALUES (10028, '老师账号13', '120', 'pbkdf2:sha256:150000$lR6FajqY$e83e639f0b2f76216a2f513f4a0d356ff0f5c85d72c88e81eefcf473859a344a', 1, NULL, '2020-03-18 17:37:15', NULL, NULL);

-- ----------------------------
-- Table structure for admin_roles
-- ----------------------------
DROP TABLE IF EXISTS `admin_roles`;
CREATE TABLE `admin_roles`  (
  `r_id` int(11) NOT NULL COMMENT '角色id,表示员工权限,1普通员工,2组长?,3主管,9老板-- 123都有增删改查权限.3能注册12权限员工,9(我全都要)',
  `r_name` char(10) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '普通员工' COMMENT '角色名字'
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of admin_roles
-- ----------------------------
INSERT INTO `admin_roles` VALUES (1, '普通员工');
INSERT INTO `admin_roles` VALUES (2, '组长');
INSERT INTO `admin_roles` VALUES (3, '主管');
INSERT INTO `admin_roles` VALUES (9, 'boss');

-- ----------------------------
-- Table structure for admins_user
-- ----------------------------
DROP TABLE IF EXISTS `admins_user`;
CREATE TABLE `admins_user`  (
  `aid` int(11) NOT NULL AUTO_INCREMENT COMMENT '内部员工id',
  `username` char(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '账号',
  `pswd` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '密码',
  `status` tinyint(4) DEFAULT 0 COMMENT '身份状态 0为未激活,1激活成功可使用,9离职(其他)',
  `create_at` datetime(0) DEFAULT CURRENT_TIMESTAMP,
  `r_id` int(11) DEFAULT NULL COMMENT '权限id',
  PRIMARY KEY (`aid`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 12 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of admins_user
-- ----------------------------
INSERT INTO `admins_user` VALUES (1, 'boss', 'pbkdf2:sha256:150000$vqMjaptw$1326cfd6afdc0425af4690011bd0af1db470a316a801d9b4b2c20f25c65e82a7', 1, '2020-03-25 14:19:37', 9);
INSERT INTO `admins_user` VALUES (2, '员工1号', 'pbkdf2:sha256:150000$3uETiTLF$20105b94e065b15e77dccd849f236f8ac1f04563d203255fa088d880c12caff8', 1, '2020-03-27 01:32:43', 1);
INSERT INTO `admins_user` VALUES (3, '员工2号', 'pbkdf2:sha256:150000$0LXsAhsS$745b6c2b4d89a340c5acbdcda3feb09c70ece4e8822fbe16871cf9dea703b6ef', 1, '2020-03-27 01:33:47', 1);
INSERT INTO `admins_user` VALUES (4, '员工3号', 'pbkdf2:sha256:150000$zzle2yCs$11a0e61facc844c23c4535b8b1a50135c904eb4c97233e52a65e74d8eb1b9d76', 1, '2020-03-27 01:33:52', 1);
INSERT INTO `admins_user` VALUES (5, '组长1号', 'pbkdf2:sha256:150000$H72U7D1D$34306053d90c21d44fe8d624357bab01e46e36380cc800710b68c78f9060c47a', 1, '2020-03-27 01:34:17', 1);
INSERT INTO `admins_user` VALUES (6, '组长2号', 'pbkdf2:sha256:150000$PMrYB4bl$c9a8431c005d3383dcf69ff3094c2a940e49aee1b7d00f3e028be9fad336af50', 1, '2020-03-27 01:34:21', 2);
INSERT INTO `admins_user` VALUES (7, '主管1号', 'pbkdf2:sha256:150000$RZArFOkb$99c072b17d7905815852584a2ba59c74c8e2402de764550cb7eaa766dbe90a92', 1, '2020-03-27 01:34:30', 1);
INSERT INTO `admins_user` VALUES (8, '主管2号', 'pbkdf2:sha256:150000$xfwU4EaJ$503b1b1aa40d36cf15962d172e9686ce8db274b84cd3ee6899da113dd175b0d6', 9, '2020-03-27 01:34:38', 1);
INSERT INTO `admins_user` VALUES (10, 'boss2号', 'pbkdf2:sha256:150000$yMpNEzOu$0657f0e77adce54d6df6afa242372adb9aa098c9fd746bb3dbb5f1aba3e8cb03', 0, '2020-03-27 01:35:08', 1);
INSERT INTO `admins_user` VALUES (11, '员工4号', 'pbkdf2:sha256:150000$o7iD4PwE$47597617bf6d62a4f12d3ac993ae9ebaf9f235ce0103c43084842b3ba26ae3d4', 9, '2020-03-27 17:03:20', 1);

-- ----------------------------
-- Table structure for catalog
-- ----------------------------
DROP TABLE IF EXISTS `catalog`;
CREATE TABLE `catalog`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '目录id',
  `cat_id` int(11) DEFAULT NULL COMMENT '外键 课程id',
  `name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '课程目录名称',
  `url` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '目录地址',
  `create_at` datetime(0) DEFAULT CURRENT_TIMESTAMP COMMENT '一个课程多个目录,根据时间排序',
  `delete_at` datetime(0) DEFAULT NULL COMMENT '删除时间,软删除',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `cat_id`(`cat_id`) USING BTREE,
  CONSTRAINT `catalog_ibfk_1` FOREIGN KEY (`cat_id`) REFERENCES `curriculums` (`cid`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of catalog
-- ----------------------------
INSERT INTO `catalog` VALUES (1, 1, 'redis 初识', '/video/test.mp4', '2020-03-15 21:51:34', NULL);
INSERT INTO `catalog` VALUES (2, 1, 'redis 类型', '/video/test1.mp4', '2020-03-15 21:52:00', NULL);
INSERT INTO `catalog` VALUES (3, 1, 'redis 事务', '/video/test2.mp4', '2020-03-15 21:52:27', NULL);
INSERT INTO `catalog` VALUES (4, 1, 'redis 异常', '/video/test3.mp4', '2020-03-15 21:53:04', NULL);
INSERT INTO `catalog` VALUES (5, 1, 'redis 异常5', '/video/test3.mp4', '2020-03-15 21:53:13', '2020-03-15 21:57:29');
INSERT INTO `catalog` VALUES (6, 1, 'redis 异常6', '/video/test3.mp4', '2020-03-15 21:53:18', '2020-03-15 21:57:14');

-- ----------------------------
-- Table structure for curriculum_comments
-- ----------------------------
DROP TABLE IF EXISTS `curriculum_comments`;
CREATE TABLE `curriculum_comments`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cid` int(11) DEFAULT NULL COMMENT '外键 课程id',
  `aid` int(11) DEFAULT NULL COMMENT '外键 用户id',
  `number` tinyint(10) DEFAULT NULL COMMENT '评价分数',
  `comment` varchar(300) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '评价',
  `create_at` datetime(0) DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `delete_at` datetime(0) DEFAULT NULL COMMENT '删除时间',
  `admin_id` int(11) DEFAULT NULL COMMENT '操作员工id',
  `open_at` datetime(0) DEFAULT NULL COMMENT '操作时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `ac_id`(`aid`, `cid`) USING BTREE,
  INDEX `curriculum_comments_ibfk_2`(`cid`) USING BTREE,
  INDEX `admin_id`(`admin_id`) USING BTREE,
  CONSTRAINT `admin_id` FOREIGN KEY (`admin_id`) REFERENCES `admins_user` (`aid`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `curriculum_comments_ibfk_1` FOREIGN KEY (`aid`) REFERENCES `accounts` (`aid`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `curriculum_comments_ibfk_2` FOREIGN KEY (`cid`) REFERENCES `curriculums` (`cid`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of curriculum_comments
-- ----------------------------
INSERT INTO `curriculum_comments` VALUES (1, 1, 10012, 8, '评价1', '2020-03-19 16:07:04', '2020-03-28 02:14:44', 1, '2020-03-28 02:14:44');
INSERT INTO `curriculum_comments` VALUES (3, 2, 10012, 8, '评价2', '2020-03-19 16:08:03', NULL, 1, '2020-03-28 02:16:42');

-- ----------------------------
-- Table structure for curriculums
-- ----------------------------
DROP TABLE IF EXISTS `curriculums`;
CREATE TABLE `curriculums`  (
  `cid` int(11) NOT NULL AUTO_INCREMENT COMMENT '课程id',
  `cname` varchar(60) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '课程名字',
  `aid` int(11) DEFAULT NULL,
  `price` float(10, 2) DEFAULT 0.00 COMMENT '价格',
  `info` text CHARACTER SET utf8 COLLATE utf8_general_ci COMMENT '课程介绍',
  `cimage` varchar(250) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '阿里云oos直传',
  `create_at` datetime(0) DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `delete_at` datetime(0) DEFAULT NULL COMMENT '删除时间',
  `open_at` datetime(0) DEFAULT NULL COMMENT '操作时间',
  `admin_id` int(11) DEFAULT NULL COMMENT '操作员工id',
  PRIMARY KEY (`cid`) USING BTREE,
  INDEX `u_id`(`aid`) USING BTREE,
  INDEX `admin_aid`(`admin_id`) USING BTREE,
  CONSTRAINT `admin_aid` FOREIGN KEY (`admin_id`) REFERENCES `admins_user` (`aid`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `curriculums_ibfk_1` FOREIGN KEY (`aid`) REFERENCES `accounts` (`aid`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of curriculums
-- ----------------------------
INSERT INTO `curriculums` VALUES (1, 'redis 初级教学(3)', 10006, 8.88, '包含redis类型,redis本地保存..', '/img/Ftest.jpg', '2020-03-15 17:21:29', NULL, NULL, NULL);
INSERT INTO `curriculums` VALUES (2, 'php 初级教学', 10006, 20.00, NULL, '/img/php.jpg', '2020-03-18 18:56:45', NULL, '2020-03-28 02:04:51', 1);
INSERT INTO `curriculums` VALUES (3, 'rust 垃圾回收机制教学', 10023, 60.00, '', '/img/testrust.jpg', '2020-03-22 23:00:14', NULL, NULL, NULL);
INSERT INTO `curriculums` VALUES (4, 'java Map 深入', 10022, 10.00, NULL, '/img/java.jgp', '2020-03-25 18:28:55', NULL, '2020-03-28 02:06:04', 1);
INSERT INTO `curriculums` VALUES (5, 'c++ 与windows api', 10026, 50.00, NULL, '/img/c++.jpg', '2020-03-25 18:29:45', '2020-03-28 01:57:54', '2020-03-28 01:57:54', 1);

-- ----------------------------
-- Table structure for extracts
-- ----------------------------
DROP TABLE IF EXISTS `extracts`;
CREATE TABLE `extracts`  (
  `eid` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键自增长',
  `create_at` datetime(0) DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `t_money` float(10, 2) DEFAULT NULL COMMENT '提取金额',
  `divide` float(10, 2) DEFAULT 0.05 COMMENT '站点分成,默认为5%',
  `actual_money` float(10, 2) DEFAULT NULL COMMENT '实际提成',
  `aid` int(11) DEFAULT NULL COMMENT '外键 用户id',
  `number` varchar(35) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '流水号',
  `status` int(11) DEFAULT 0 COMMENT '转账交易状态 0 为显示转账但是未到达,1为转账成功,2为转账失败',
  PRIMARY KEY (`eid`) USING BTREE,
  INDEX `aid`(`aid`) USING BTREE,
  CONSTRAINT `extracts_ibfk_1` FOREIGN KEY (`aid`) REFERENCES `accounts` (`aid`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of extracts
-- ----------------------------
INSERT INTO `extracts` VALUES (1, '2020-03-18 16:00:43', 0.30, 0.05, 5.70, 10006, '9cd2afeae93a4b14818c7c3b6d5074ac', 0);
INSERT INTO `extracts` VALUES (2, '2020-03-18 16:51:09', 0.30, 0.05, 5.70, 10006, 'fb1b792bc2594d39851d6ae233624b50', 0);
INSERT INTO `extracts` VALUES (3, '2020-03-18 16:59:05', 0.30, 0.05, 5.70, 10006, '4ee59bd0a39f40829384cd241d27e19b', 0);
INSERT INTO `extracts` VALUES (4, '2020-03-18 16:59:14', 0.30, 0.05, 5.70, 10006, 'dc953979057f49ee812c889f9673af85', 0);
INSERT INTO `extracts` VALUES (5, '2020-03-18 16:59:19', 0.30, 0.05, 5.70, 10006, '49a7ad5e8cdb4b399322dd5e01b3c06b', 0);
INSERT INTO `extracts` VALUES (6, '2020-03-18 16:59:20', 0.30, 0.05, 5.70, 10006, 'ece9f61827a94a159959cf71070c84c0', 0);
INSERT INTO `extracts` VALUES (7, '2020-03-18 16:59:22', 0.30, 0.05, 5.70, 10006, '0f934d8af497460f8091d499da1c382e', 0);

-- ----------------------------
-- Table structure for money
-- ----------------------------
DROP TABLE IF EXISTS `money`;
CREATE TABLE `money`  (
  `aid` int(11) DEFAULT NULL COMMENT '外键用户表id,唯一',
  `money` float(10, 2) DEFAULT 0.00 COMMENT '金钱',
  `version` int(11) DEFAULT NULL COMMENT '乐观锁,版本控制',
  UNIQUE INDEX `aid`(`aid`) USING BTREE,
  CONSTRAINT `money_ibfk_1` FOREIGN KEY (`aid`) REFERENCES `accounts` (`aid`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of money
-- ----------------------------
INSERT INTO `money` VALUES (10006, 34.40, 7);

-- ----------------------------
-- Table structure for purchases
-- ----------------------------
DROP TABLE IF EXISTS `purchases`;
CREATE TABLE `purchases`  (
  `cid` int(11) DEFAULT NULL COMMENT '外键 课程id',
  `aid` int(11) DEFAULT NULL COMMENT '外键 用户id',
  `status` tinyint(1) DEFAULT NULL COMMENT '订单状态,默认为0未支付 支付为1',
  `price` float(10, 2) DEFAULT NULL COMMENT '订单当时价格,数量不考虑因为是类似网易云课堂这种 只能买一份',
  `number` varchar(40) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT 'uuid流水号',
  `create_at` datetime(0) DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  INDEX `cid`(`cid`) USING BTREE,
  INDEX `aid`(`aid`) USING BTREE,
  CONSTRAINT `purchases_ibfk_1` FOREIGN KEY (`aid`) REFERENCES `accounts` (`aid`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `purchases_ibfk_2` FOREIGN KEY (`cid`) REFERENCES `curriculums` (`cid`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for shopping_carts
-- ----------------------------
DROP TABLE IF EXISTS `shopping_carts`;
CREATE TABLE `shopping_carts`  (
  `aid` int(11) DEFAULT NULL COMMENT '外键 用户id',
  `cid` int(11) DEFAULT NULL COMMENT '外键 课程id',
  `number` int(11) DEFAULT 1 COMMENT '课程数量,但是是网易云课堂类似的,默认就是1买把...',
  `price` float(10, 2) DEFAULT 0.00 COMMENT '购买时价格',
  `create_at` datetime(0) DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '创建时间',
  INDEX `uid`(`aid`) USING BTREE,
  INDEX `cid`(`cid`) USING BTREE,
  CONSTRAINT `shopping_carts_ibfk_1` FOREIGN KEY (`aid`) REFERENCES `accounts` (`aid`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `shopping_carts_ibfk_2` FOREIGN KEY (`cid`) REFERENCES `curriculums` (`cid`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of shopping_carts
-- ----------------------------
INSERT INTO `shopping_carts` VALUES (10008, 1, 1, 0.00, '2020-03-17 18:13:04');
INSERT INTO `shopping_carts` VALUES (10009, 2, 1, 20.00, '2020-03-18 18:59:20');
INSERT INTO `shopping_carts` VALUES (10012, 1, 1, 0.00, '2020-03-20 00:38:23');
INSERT INTO `shopping_carts` VALUES (10012, 2, 1, 0.00, '2020-03-20 16:33:48');

-- ----------------------------
-- Table structure for use_collections
-- ----------------------------
DROP TABLE IF EXISTS `use_collections`;
CREATE TABLE `use_collections`  (
  `aid` int(11) DEFAULT NULL COMMENT '外键 用户id',
  `cid` int(11) DEFAULT NULL COMMENT '外键 课程id',
  `create_at` datetime(0) DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `delete_at` datetime(0) DEFAULT NULL COMMENT '删除时间,软删除',
  INDEX `cid`(`cid`) USING BTREE,
  INDEX `aid`(`aid`) USING BTREE,
  CONSTRAINT `use_collections_ibfk_1` FOREIGN KEY (`cid`) REFERENCES `curriculums` (`cid`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `use_collections_ibfk_2` FOREIGN KEY (`aid`) REFERENCES `accounts` (`aid`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of use_collections
-- ----------------------------
INSERT INTO `use_collections` VALUES (10012, 1, '2020-03-19 15:39:53', NULL);
INSERT INTO `use_collections` VALUES (10012, 2, '2020-03-19 15:40:15', '2020-03-19 16:02:34');

SET FOREIGN_KEY_CHECKS = 1;
