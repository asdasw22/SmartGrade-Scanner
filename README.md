# SmartGrade Scanner

تطبيق iOS مبني بـ **SwiftUI** لمساعدة المعلمين على مسح أوراق الإجابات بنظام **OMR**، قراءة رقم الطالب والإجابات من الصور، تصحيح الاختبارات تلقائيًا، مراجعة النتائج يدويًا عند الحاجة، وعرض إحصائيات الأداء وتصدير النتائج بصيغة CSV.

---

## نظرة عامة

يوفر SmartGrade Scanner واجهة عربية/إنجليزية لإدارة الاختبارات والطلاب والصفوف، ثم مسح أوراق الإجابة باستخدام الكاميرا أو ماسح المستندات أو الصور الموجودة في مكتبة الصور. بعد المسح يقوم التطبيق بتحليل الدوائر المظللة، مطابقة الطالب إن كان مسجلًا، حساب الدرجة، ثم حفظ النتيجة داخل التطبيق.

المشروع لا يعتمد على خادم خارجي أو قاعدة بيانات خارجية؛ البيانات تحفظ محليًا داخل التطبيق باستخدام `UserDefaults`.

---

## الميزات

- مسح أوراق الإجابة باستخدام:
  - ماسح المستندات من Apple عبر `VisionKit`.
  - كاميرا النظام.
  - اختيار صورة من مكتبة الصور عبر `PhotosUI`.
- قراءة رقم الطالب من شبكة OMR.
- قراءة إجابات الاختيار من متعدد A/B/C/D/E.
- دعم قوالب افتراضية:
  - قالب 20 سؤالًا.
  - قالب 50 سؤالًا.
- إنشاء وإدارة:
  - الاختبارات.
  - الطلاب.
  - الصفوف/الفصول.
  - مفاتيح الإجابة.
- تصحيح تلقائي وحساب:
  - الدرجة النهائية.
  - النسبة المئوية.
  - عدد الإجابات الصحيحة والخاطئة والفارغة والمتعددة.
- شاشة مراجعة بعد المسح لتعديل رقم الطالب أو الإجابات قبل حفظ النتيجة.
- إحصائيات للاختبارات تشمل:
  - عدد الطلاب الذين تم مسح أوراقهم.
  - المتوسط.
  - أعلى درجة.
  - نسبة النجاح.
  - توزيع الدرجات.
  - تحليل الأسئلة.
- تصدير النتائج بصيغة CSV ومشاركتها من داخل iOS.
- دعم الاتجاه من اليمين إلى اليسار عند استخدام العربية.
- بيانات تجريبية افتراضية عند أول تشغيل.

---

## التقنيات المستخدمة

- **Swift 5**
- **SwiftUI**
- **UIKit**
- **VisionKit** لمسح المستندات.
- **PhotosUI** لاختيار الصور.
- **Combine** لإدارة الحالة.
- **CoreGraphics** لمعالجة الصور وقراءة قيم البكسل.
- **UserDefaults** لحفظ البيانات محليًا.
- **GitHub Actions** لبناء أرشيف iOS وإنتاج IPA غير موقّع.

لا توجد حزم خارجية مطلوبة في المشروع حاليًا.

---

## المتطلبات

- macOS لتشغيل Xcode وبناء تطبيق iOS.
- Xcode يدعم iOS 17 أو أحدث.
- iOS 17.0 أو أحدث حسب إعدادات المشروع.
- جهاز iPhone أو iPad أو iOS Simulator.
- لاستخدام الكاميرا فعليًا يفضل جهاز حقيقي، لأن بعض وظائف الكاميرا/ماسح المستندات قد لا تعمل بالكامل على المحاكي.

إعدادات المشروع الحالية:

- اسم التطبيق: `SmartGrade Scanner`
- اسم الـ Scheme: `SmartGradeScanner`
- Bundle Identifier: `com.smartgrade.scanner`
- Deployment Target: `iOS 17.0`
- الأجهزة المستهدفة: iPhone و iPad

---

## تشغيل المشروع محليًا

1. افتح الملف التالي باستخدام Xcode:

   ```text
   SmartGradeScanner.xcodeproj
   ```

2. اختر Scheme باسم:

   ```text
   SmartGradeScanner
   ```

3. اختر جهاز تشغيل:
   - iPhone Simulator للتجربة العامة.
   - iPhone/iPad حقيقي لتجربة الكاميرا وماسح المستندات.

4. اضغط Run من Xcode أو استخدم الاختصار:

   ```text
   Cmd + R
   ```

---

## البناء من سطر الأوامر

يمكن بناء المشروع على macOS باستخدام `xcodebuild`:

```bash
xcodebuild \
  -project SmartGradeScanner.xcodeproj \
  -scheme SmartGradeScanner \
  -configuration Debug \
  -sdk iphonesimulator \
  build
```

لبناء أرشيف iOS بدون توقيع:

```bash
xcodebuild archive \
  -project SmartGradeScanner.xcodeproj \
  -scheme SmartGradeScanner \
  -configuration Release \
  -sdk iphoneos \
  -destination 'generic/platform=iOS' \
  -archivePath build/SmartGradeScanner.xcarchive \
  CODE_SIGNING_ALLOWED=NO \
  CODE_SIGNING_REQUIRED=NO \
  CODE_SIGN_IDENTITY="" \
  DEVELOPMENT_TEAM="" \
  SKIP_INSTALL=NO \
  clean archive
```

---

## بناء IPA عبر GitHub Actions

يوجد Workflow جاهز في:

```text
.github/workflows/build-ios-ipa.yml
```

يقوم workflow بالتالي:

1. تشغيل البناء على `macos-15`.
2. حل اعتماديات Swift Packages إن وجدت.
3. بناء Archive بدون Code Signing.
4. إنشاء ملف IPA غير موقّع:

   ```text
   build/SmartGradeScanner-unsigned.ipa
   ```

5. رفع المخرجات كـ artifacts:
   - `SmartGradeScanner-unsigned-ipa`
   - `SmartGradeScanner-xcarchive`

> ملاحظة: الـ IPA الناتج غير موقّع، لذلك يحتاج إلى توقيع مناسب قبل التثبيت على أجهزة حقيقية خارج بيئة التطوير.

---

## طريقة الاستخدام

1. افتح التطبيق.
2. من تبويب **الاختبارات** أنشئ أو اختر اختبارًا وحدد مفتاح الإجابة.
3. تأكد من وجود الطلاب والصفوف في تبويبي **الطلاب** و **الصفوف**.
4. انتقل إلى تبويب **المسح**.
5. اختر الاختبار المطلوب.
6. التقط ورقة الإجابة أو اختر صورة من مكتبة الصور.
7. اضغط زر التحليل عند ظهور الصورة.
8. راجع النتيجة في شاشة المراجعة:
   - رقم الطالب.
   - الإجابات المقروءة.
   - الدرجة والنسبة.
   - أي إجابات تحتاج مراجعة.
9. احفظ النتيجة.
10. انتقل إلى **الإحصائيات** لمتابعة أداء الطلاب وتصدير CSV.

---

## بنية المشروع

```text
SmartGradeScanner/
├── App/
│   └── SmartGradeScannerApp.swift
├── Models/
│   └── OMRModels.swift
├── Resources/
│   └── Assets.xcassets/
├── Services/
│   ├── DefaultTemplateFactory.swift
│   ├── DocumentScannerService.swift
│   ├── ExportServices.swift
│   ├── GradingService.swift
│   ├── OMRProcessor.swift
│   ├── SampleDataSeeder.swift
│   ├── SmartGradeStore.swift
│   └── StatisticsService.swift
└── Views/
    ├── AnalyticsView.swift
    ├── ClassroomsView.swift
    ├── DesignSystem.swift
    ├── ExamsView.swift
    ├── RootView.swift
    ├── ScannerView.swift
    ├── ScanReviewView.swift
    ├── StudentsView.swift
    └── TemplatesView.swift
```

---

## شرح مختصر لأهم الملفات

- `SmartGradeScanner/App/SmartGradeScannerApp.swift`  
  نقطة دخول التطبيق وحقن `SmartGradeStore` في البيئة.

- `SmartGradeScanner/Models/OMRModels.swift`  
  يحتوي نماذج البيانات الأساسية مثل الطالب، الصف، الاختبار، القالب، النتيجة، وإجابات OMR.

- `SmartGradeScanner/Services/SmartGradeStore.swift`  
  مسؤول عن إدارة الحالة وحفظ البيانات محليًا في `UserDefaults`.

- `SmartGradeScanner/Services/OMRProcessor.swift`  
  مسؤول عن تحويل الصورة إلى تدرج رمادي، تحليل جودة الصورة، قراءة رقم الطالب، وقراءة الإجابات.

- `SmartGradeScanner/Services/GradingService.swift`  
  مسؤول عن حساب الدرجات وإعادة الحساب بعد التعديل اليدوي.

- `SmartGradeScanner/Services/StatisticsService.swift`  
  يحسب إحصائيات الاختبار وتوزيع الدرجات وتحليل الأسئلة.

- `SmartGradeScanner/Services/ExportServices.swift`  
  يولد CSV ويعرض نافذة المشاركة في iOS.

- `SmartGradeScanner/Views/ScannerView.swift`  
  واجهة المسح واختيار الصور وتشغيل المعالجة.

- `SmartGradeScanner/Views/ScanReviewView.swift`  
  شاشة مراجعة نتيجة المسح قبل الحفظ.

---

## الخصوصية والبيانات

- البيانات تحفظ محليًا على الجهاز باستخدام `UserDefaults`.
- لا يوجد إرسال بيانات إلى خادم خارجي في الكود الحالي.
- التطبيق يطلب صلاحيات:
  - الكاميرا لمسح أوراق الإجابة.
  - مكتبة الصور لاستيراد صور أوراق الإجابة.

---

## ملاحظات مهمة

- جودة قراءة OMR تعتمد على وضوح الصورة، الإضاءة، ومحاذاة الورقة مع القالب المستخدم.
- القوالب الافتراضية مبنية على إحداثيات نسبية داخل صفحة بنسبة A4 تقريبًا.
- إذا ظهرت إجابات ضعيفة أو متعددة أو غير مؤكدة، سيعلّم التطبيق النتيجة بأنها تحتاج مراجعة يدوية.
- ملف IPA الذي ينتجه GitHub Actions غير موقّع، ولا يعتبر ملف توزيع نهائي على App Store.

---

## استكشاف الأخطاء

### الكاميرا لا تعمل على المحاكي

استخدم جهاز iPhone أو iPad حقيقي، لأن المحاكي لا يدعم كل وظائف الكاميرا وماسح المستندات.

### لا تظهر نتائج دقيقة بعد المسح

تأكد من:

- استخدام قالب مطابق لورقة الإجابة.
- أن الورقة واضحة وغير مائلة قدر الإمكان.
- أن الدوائر مظللة بوضوح.
- عدم وجود ظلال قوية أو إضاءة ضعيفة.

### فشل البناء بسبب التوقيع

أضف Team ID من إعدادات Xcode إذا أردت التشغيل على جهاز حقيقي، أو استخدم إعدادات البناء بدون توقيع كما في workflow.

---

## الترخيص

لا يوجد ملف ترخيص مرفق في المشروع حاليًا. أضف ملف `LICENSE` إذا كنت تريد تحديد شروط الاستخدام أو النشر.