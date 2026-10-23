from werkzeug.security import check_password_hash

# اختبار كلمة المرور
hashed_password = "scrypt:32768:8:1$rPYZonRB4GZ0IWHF$11b94a4f5f9833d470de1cab7570d5a974de07c8a222ef2fca90da3e1b068a936312b4958a9cc90e3af58e188cba70d2b3e2f01403c936cfed0c48e43ee32603"
password = "12345"

if check_password_hash(hashed_password, password):
    print("كلمة السر صحيحة ✅")
else:
    print("كلمة السر غلط ❌")
