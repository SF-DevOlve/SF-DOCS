-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le : ven. 17 mai 2024 à 03:56
-- Version du serveur : 10.4.27-MariaDB
-- Version de PHP : 8.1.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `vishing`
--

-- --------------------------------------------------------

--
-- Structure de la table `categories`
--

CREATE TABLE `categories` (
  `category_id` int(11) NOT NULL,
  `category_name` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `categories`
--

INSERT INTO `categories` (`category_id`, `category_name`) VALUES
(1, 'Menaces financières'),
(2, 'Informations personnelles'),
(3, 'Hameçonnage');

-- --------------------------------------------------------

--
-- Structure de la table `categories_ar`
--

CREATE TABLE `categories_ar` (
  `category_id` int(11) NOT NULL,
  `category_name` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `categories_ar`
--

INSERT INTO `categories_ar` (`category_id`, `category_name`) VALUES
(1, 'تهديدات مالية'),
(2, 'معلومات شخصية'),
(3, 'التصيد');

-- --------------------------------------------------------

--
-- Structure de la table `orders`
--

CREATE TABLE `orders` (
  `order_id` int(11) NOT NULL,
  `category_id` int(11) DEFAULT NULL,
  `sentence` text DEFAULT NULL,
  `hotwords` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `orders`
--

INSERT INTO `orders` (`order_id`, `category_id`, `sentence`, `hotwords`) VALUES
(1, 1, 'Bonjour, je suis [nom du fraudeur], un agent de la banque [nom de la banque]. Nous avons remarqué une activité suspecte sur votre compte et nous devons vérifier votre identité.', 'agent de la banque, activité suspecte, vérification d\'identité'),
(2, 1, 'Votre carte bancaire a été compromise et des transactions frauduleuses ont été effectuées. Veuillez nous communiquer immédiatement le numéro de votre carte et la date d\'expiration', 'carte bancaire compromise, transactions frauduleuses, numéro de carte, date d\'expiration'),
(3, 1, 'Vous avez été pré-approuvé pour un crédit incroyable ! Appelez-nous au [numéro de téléphone frauduleux] pour en savoir plus.', 'crédit pré-approuvé, numéro de téléphone frauduleux'),
(4, 1, 'Votre facture est en retard et des frais de retard vont s\'appliquer. Veuillez effectuer un paiement immédiat en appelant le [numéro de téléphone frauduleux]', 'facture en retard, frais de retard, paiement immédiat'),
(5, 2, 'Bonjour, je suis [nom du fraudeur], un représentant de [nom de l\'entreprise]. Votre commande est en cours d\'expédition et nous avons besoin de confirmer votre adresse de livraison.', 'commande en cours d\'expédition, confirmation d\'adresse de livraison'),
(6, 2, 'Un colis vous attend à votre bureau de poste local. Veuillez nous fournir votre code postal et votre numéro de téléphone pour vérifier son identité.', 'colis en attente, bureau de poste local, code postal, numéro de téléphone, vérification d\'identité'),
(7, 2, 'Nous avons détecté une activité suspecte sur votre compte [nom du service]. Veuillez changer votre mot de passe en appelant le [numéro de téléphone frauduleux].', 'activité suspecte, changement de mot de passe, numéro de téléphone frauduleux'),
(8, 2, 'Pour des raisons de sécurité, nous vous demandons de vérifier votre identité en nous fournissant votre date de naissance et votre numéro de sécurité sociale.', 'raisons de sécurité, vérification d\'identité, date de naissance, numéro de sécurité sociale'),
(9, 2, 'Nous mettons à jour nos dossiers et avons besoin de confirmer vos informations personnelles. Veuillez nous les communiquer par téléphone.', 'mise à jour des dossiers, confirmation des informations personnelles'),
(10, 3, 'Félicitations ! Vous avez gagné un voyage tout inclus ! Appelez-nous au [numéro de téléphone frauduleux] pour réclamer votre prix.', 'Félicitations, voyage tout inclus, numéro de téléphone frauduleux, réclamation de prix'),
(11, 3, 'Participez à notre sondage rapide et courez la chance de gagner un nouveau smartphone. Répondez à quelques questions par téléphone.', 'sondage rapide, smartphone, questions par téléphone'),
(12, 3, 'Investissez dans cette opportunité exclusive et garantissez votre avenir financier. Appelez nos experts financiers au [numéro de téléphone frauduleux]', 'investissement exclusif, avenir financier, experts financiers, numéro de téléphone frauduleux'),
(13, 3, 'Votre ordinateur est infecté par un virus dangereux. Appelez notre service d\'assistance technique au [numéro de téléphone frauduleux] pour le supprimer.', 'virus dangereux, ordinateur infecté, assistance technique, numéro de téléphone frauduleux'),
(14, 3, 'Votre logiciel est obsolète et vous expose à des risques de sécurité. Mettez à jour votre logiciel en appelant le [numéro de téléphone frauduleux].', 'logiciel obsolète, risques de sécurité, mise à jour du logiciel, numéro de téléphone frauduleux');

-- --------------------------------------------------------

--
-- Structure de la table `orders_ar`
--

CREATE TABLE `orders_ar` (
  `order_id` int(11) NOT NULL,
  `category_id` int(11) DEFAULT NULL,
  `sentence` text DEFAULT NULL,
  `hotwords` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `orders_ar`
--

INSERT INTO `orders_ar` (`order_id`, `category_id`, `sentence`, `hotwords`) VALUES
(1, 1, 'مرحبًا، أنا [اسم النصاب]، وكيل بنك [اسم البنك]. لقد لاحظنا نشاطًا مشبوهًا في حسابك ونحتاج إلى التحقق من هويتك.', 'وكيل بنك, نشاط مشبوه, التحقق من هويتك'),
(2, 1, 'تمت إختراق بطاقتك البنكية وتمت إجراء معاملات غير مشروعة. يرجى تزويدنا على الفور برقم بطاقتك وتاريخ الانتهاء', 'بطاقة بنكية مخترقة, معاملات غير مشروعة, رقم البطاقة, تاريخ الانتهاء'),
(3, 1, 'لقد تمت الموافقة المسبقة عليك للحصول على قرض رائع! اتصل بنا على [رقم الهاتف المزور] لمعرفة المزيد.', 'قرض مسبق الموافقة, رقم الهاتف المزور'),
(4, 1, 'فاتورتك متأخرة وسيتم تطبيق رسوم تأخير. يرجى إجراء الدفع على الفور عن طريق الاتصال بـ [رقم الهاتف المزور]', 'فاتورة متأخرة, رسوم تأخير, دفع فوري'),
(5, 2, 'مرحبًا، أنا [اسم النصاب]، ممثل [اسم الشركة]. طلبك قيد الشحن ونحتاج إلى تأكيد عنوان التسليم الخاص بك.', 'طلب قيد الشحن, تأكيد عنوان التسليم'),
(6, 2, 'ينتظرك طرد في مكتب البريد المحلي الخاص بك. يرجى تزويدنا بالرمز البريدي ورقم الهاتف الخاص بك للتحقق من هويته.', 'طرد في الانتظار, مكتب بريد محلي, الرمز البريدي, رقم الهاتف, التحقق من الهوية'),
(7, 2, 'لقد اكتشفنا نشاطًا مشبوهًا على حسابك في [اسم الخدمة]. يرجى تغيير كلمة المرور الخاصة بك عن طريق الاتصال بـ [رقم الهاتف المزور].', 'نشاط مشبوه, تغيير كلمة المرور, رقم الهاتف المزور'),
(8, 2, 'من أجل الأمان، نطلب منك التحقق من هويتك من خلال تقديم تاريخ ميلادك ورقم الضمان الاجتماعي الخاص بك.', 'أسباب الأمان, التحقق من الهوية, تاريخ الميلاد, رقم الضمان الاجتماعي'),
(9, 2, 'نقوم بتحديث سجلاتنا ونحتاج إلى تأكيد معلوماتك الشخصية. يرجى تقديمها لنا عبر الهاتف.', 'تحديث السجلات, تأكيد المعلومات الشخصية'),
(10, 3, 'تهانينا! لقد فزت برحلة مجانية متضمنة كل شيء! اتصل بنا على [رقم الهاتف المزور] لاستلام جائزتك.', 'تهاني, رحلة مجانية, رقم الهاتف المزور, استلام الجائزة'),
(11, 3, 'شارك في استطلاعنا السريع واربح هاتف ذكي جديد. أجب على بعض الأسئلة عبر الهاتف.', 'استطلاع سريع, هاتف ذكي, أسئلة عبر الهاتف'),
(12, 3, 'استثمر في هذه الفرصة الحصرية وضمن مستقبلك المالي. اتصل بخبرائنا الماليين على [رقم الهاتف المزور]', 'استثمار حصري, مستقبل مالي, خبراء ماليين, رقم الهاتف المزور'),
(13, 3, 'جهاز الكمبيوتر الخاص بك مصاب بفيروس خطير. اتصل بخدمة المساعدة الفنية الخاصة بنا على [رقم الهاتف المزور] لإزالته.', 'فيروس خطير, كمبيوتر مصاب, مساعدة فنية, رقم الهاتف المزور'),
(14, 3, 'البرنامج الخاص بك قديم ويعرضك لمخاطر الأمان. قم بتحديث برنامجك عن طريق الاتصال بـ [رقم الهاتف المزور].', 'برنامج قديم, مخاطر أمان, تحديث البرنامج, رقم الهاتف المزور');

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`category_id`);

--
-- Index pour la table `categories_ar`
--
ALTER TABLE `categories_ar`
  ADD PRIMARY KEY (`category_id`);

--
-- Index pour la table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`order_id`),
  ADD KEY `category_id` (`category_id`);

--
-- Index pour la table `orders_ar`
--
ALTER TABLE `orders_ar`
  ADD PRIMARY KEY (`order_id`),
  ADD KEY `category_id` (`category_id`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `orders`
--
ALTER TABLE `orders`
  MODIFY `order_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT pour la table `orders_ar`
--
ALTER TABLE `orders_ar`
  MODIFY `order_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `categories` (`category_id`);

--
-- Contraintes pour la table `orders_ar`
--
ALTER TABLE `orders_ar`
  ADD CONSTRAINT `orders_ar_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `categories_ar` (`category_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
