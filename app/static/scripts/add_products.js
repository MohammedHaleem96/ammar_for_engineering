// وظيفة لإظهار خصائص المنتج بناءً على نوعه
function showProductProperties(productType) {
    // إخفاء كل الخصائص
    const allProperties = document.querySelectorAll('.product-properties');
    allProperties.forEach(properties => properties.style.display = 'none');

    // عرض الخصائص المطلوبة بناءً على نوع المنتج
    if (productType === 'محول طاقة') {
        document.getElementById('inverterProperties').style.display = 'block';
    } else if (productType === 'بطارية') {
        document.getElementById('batteryProperties').style.display = 'block';
    } else if (productType === 'لوح شمسي') {
        document.getElementById('panelProperties').style.display = 'block';
    } else if (productType === 'قاطع كهربائي') {
        document.getElementById('breakerProperties').style.display = 'block';
    }
}

// وظيفة للتأكد من صحة البيانات قبل الإرسال
function prepareForm(form) {
    // التحقق من إدخال البيانات المطلوبة
    const nameField = form.querySelector('#name');
    const priceField = form.querySelector('#price');
    
    if (!nameField.value.trim()) {
        alert('يرجى إدخال اسم المنتج');
        return false;
    }
    
    if (priceField.value <= 0) {
        alert('يرجى إدخال سعر صحيح للمنتج');
        return false;
    }
    
    return true; // السماح بإرسال النموذج
}

// تحميل الوظائف عند فتح الصفحة
document.addEventListener('DOMContentLoaded', () => {
    const productTypeSelect = document.getElementById('productType');
    if (productTypeSelect) {
        // إظهار الخصائص عند تغيير نوع المنتج
        productTypeSelect.addEventListener('change', (event) => {
            showProductProperties(event.target.value);
        });
    }
});
