/*
 Navicat Premium Data Transfer

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 80037 (8.0.37)
 Source Host           : localhost:3306
 Source Schema         : takeaway

 Target Server Type    : MySQL
 Target Server Version : 80037 (8.0.37)
 File Encoding         : 65001

 Date: 27/06/2024 08:08:35
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for dispatcher
-- ----------------------------
DROP TABLE IF EXISTS `dispatcher`;
CREATE TABLE `dispatcher`  (
  `dispatcher_id` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `dispatcher_name` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `dispatcher_phone` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  PRIMARY KEY (`dispatcher_id`) USING BTREE,
  UNIQUE INDEX `dispatcher_id`(`dispatcher_id` ASC) USING BTREE,
  INDEX `dispatcher_name`(`dispatcher_name` ASC) USING BTREE,
  INDEX `dispatcher_phone`(`dispatcher_phone` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for fastfood_shop
-- ----------------------------
DROP TABLE IF EXISTS `fastfood_shop`;
CREATE TABLE `fastfood_shop`  (
  `shop_name` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `price` int NOT NULL COMMENT '价格',
  `m_sale_v` int NOT NULL COMMENT '销售量',
  PRIMARY KEY (`shop_name`) USING BTREE,
  UNIQUE INDEX `shop_name`(`shop_name` ASC) USING BTREE,
  INDEX `price`(`price` ASC) USING BTREE,
  INDEX `m_sale_v`(`m_sale_v` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of fastfood_shop
-- ----------------------------
INSERT INTO `fastfood_shop` VALUES ('二先生炸肉', 10, 102);
INSERT INTO `fastfood_shop` VALUES ('大先生小碗菜', 20, 200);
INSERT INTO `fastfood_shop` VALUES ('柠檬队长炸鸡', 15, 100);
INSERT INTO `fastfood_shop` VALUES ('添水麻辣烫', 18, 103);
INSERT INTO `fastfood_shop` VALUES ('粒粒香炒饭', 16, 61);
INSERT INTO `fastfood_shop` VALUES ('老郑烤肉', 20, 52);
INSERT INTO `fastfood_shop` VALUES ('蜜饯滑蛋饭', 16, 99);
INSERT INTO `fastfood_shop` VALUES ('踏思腚汉堡', 18, 101);

-- ----------------------------
-- Table structure for oorder
-- ----------------------------
DROP TABLE IF EXISTS `oorder`;
CREATE TABLE `oorder`  (
  `order_id` int NOT NULL AUTO_INCREMENT,
  `shop_name` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `order_money` int NOT NULL,
  `cons_phone` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `cons_name` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `cons_addre` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `checked` int NULL DEFAULT 0,
  `create_time` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`order_id`) USING BTREE,
  UNIQUE INDEX `order_id`(`order_id` ASC) USING BTREE,
  INDEX `shop_name`(`shop_name` ASC) USING BTREE,
  INDEX `order_money`(`order_money` ASC) USING BTREE,
  INDEX `cons_phone`(`cons_phone` ASC) USING BTREE,
  INDEX `cons_name`(`cons_name` ASC) USING BTREE,
  INDEX `cons_addre`(`cons_addre` ASC) USING BTREE,
  INDEX `checked`(`checked` ASC) USING BTREE,
  INDEX `create_time`(`create_time` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 18 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of oorder
-- ----------------------------
INSERT INTO `oorder` VALUES (17, '二先生炸肉', 10, '19552312067', '宋子杰', '梅二15号楼', 0, '2024-06-27 00:01:02', NULL);

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `username` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `password` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `telephone` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `role` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `id`(`id` ASC) USING BTREE COMMENT '主键索引，选UNIQUE',
  INDEX `username`(`username` ASC) USING BTREE,
  INDEX `password`(`password` ASC) USING BTREE,
  INDEX `telephone`(`telephone` ASC) USING BTREE,
  INDEX `role`(`role` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES (1, '808', 'Songzijie1', '19552312067', 0);
INSERT INTO `user` VALUES (2, 'Administrator', 'Songzijie1', '19552312068', 1);

-- ----------------------------
-- Table structure for user_msg
-- ----------------------------
DROP TABLE IF EXISTS `user_msg`;
CREATE TABLE `user_msg`  (
  `id` int UNSIGNED NULL DEFAULT NULL,
  `real_name` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL,
  `sex` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL,
  `age` int NULL DEFAULT NULL,
  `mail` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL,
  `phone` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `user_name` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  INDEX `userid`(`id` ASC) USING BTREE,
  INDEX `real_name`(`real_name` ASC) USING BTREE,
  INDEX `sex`(`sex` ASC) USING BTREE,
  INDEX `age`(`age` ASC) USING BTREE,
  INDEX `mail`(`mail` ASC) USING BTREE,
  INDEX `phone`(`phone` ASC) USING BTREE,
  INDEX `user_name`(`user_name` ASC) USING BTREE,
  CONSTRAINT `userid` FOREIGN KEY (`id`) REFERENCES `user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of user_msg
-- ----------------------------
INSERT INTO `user_msg` VALUES (1, '宋子杰', '男', 21, 'Zi_Yan416@163.com', '19552312067', '808');
INSERT INTO `user_msg` VALUES (2, NULL, NULL, NULL, NULL, '19552312068', 'Administrator');

-- ----------------------------
-- Table structure for wuliu
-- ----------------------------
DROP TABLE IF EXISTS `wuliu`;
CREATE TABLE `wuliu`  (
  `order_id` int NOT NULL COMMENT '订单的编号',
  `cons_phone` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `disp_id` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `deliver_time` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `ended` int NOT NULL DEFAULT 0 COMMENT '是否结束',
  PRIMARY KEY (`order_id`) USING BTREE,
  UNIQUE INDEX `order_id`(`order_id` ASC) USING BTREE,
  INDEX `cons_phone`(`cons_phone` ASC) USING BTREE,
  INDEX `disp_id`(`disp_id` ASC) USING BTREE,
  INDEX `deliver_time`(`deliver_time` ASC) USING BTREE,
  INDEX `ended`(`ended` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of wuliu
-- ----------------------------

-- ----------------------------
-- View structure for sended_order
-- ----------------------------
DROP VIEW IF EXISTS `sended_order`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `sended_order` AS select `o`.`order_id` AS `order_id`,`o`.`shop_name` AS `shop_name`,`o`.`order_money` AS `order_money`,`o`.`cons_phone` AS `cons_phone`,`o`.`cons_name` AS `cons_name`,`o`.`cons_addre` AS `cons_addre`,`w`.`disp_id` AS `disp_id`,`w`.`deliver_time` AS `deliver_time`,`d`.`dispatcher_phone` AS `dispatcher_phone` from ((`oorder` `o` join `wuliu` `w` on((`o`.`order_id` = `w`.`order_id`))) join `dispatcher` `d` on((`w`.`disp_id` = `d`.`dispatcher_id`))) where (`o`.`checked` = 2);

-- ----------------------------
-- View structure for sending_order
-- ----------------------------
DROP VIEW IF EXISTS `sending_order`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `sending_order` AS select `o`.`order_id` AS `order_id`,`o`.`shop_name` AS `shop_name`,`o`.`order_money` AS `order_money`,`o`.`cons_phone` AS `cons_phone`,`o`.`cons_name` AS `cons_name`,`o`.`cons_addre` AS `cons_addre`,`w`.`disp_id` AS `disp_id`,`w`.`deliver_time` AS `deliver_time`,`d`.`dispatcher_phone` AS `dispatcher_phone` from ((`oorder` `o` join `wuliu` `w` on((`o`.`order_id` = `w`.`order_id`))) join `dispatcher` `d` on((`w`.`disp_id` = `d`.`dispatcher_id`))) where (`o`.`checked` = 1);

-- ----------------------------
-- Triggers structure for table oorder
-- ----------------------------
DROP TRIGGER IF EXISTS `order_insert_sale`;
delimiter ;;
CREATE TRIGGER `order_insert_sale` AFTER INSERT ON `oorder` FOR EACH ROW BEGIN
UPDATE fastfood_shop
SET fastfood_shop.m_sale_v=fastfood_shop.m_sale_v+1
WHERE fastfood_shop.shop_name=new.shop_name;
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table oorder
-- ----------------------------
DROP TRIGGER IF EXISTS `order_delete_sale`;
delimiter ;;
CREATE TRIGGER `order_delete_sale` AFTER DELETE ON `oorder` FOR EACH ROW BEGIN
UPDATE fastfood_shop
SET fastfood_shop.m_sale_v=fastfood_shop.m_sale_v-1
WHERE fastfood_shop.shop_name=old.shop_name;
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table wuliu
-- ----------------------------
DROP TRIGGER IF EXISTS `wuliu_insert`;
delimiter ;;
CREATE TRIGGER `wuliu_insert` AFTER INSERT ON `wuliu` FOR EACH ROW BEGIN
UPDATE oorder
SET oorder.checked=1
WHERE oorder.order_id=new.order_id;
END
;;
delimiter ;

SET FOREIGN_KEY_CHECKS = 1;
