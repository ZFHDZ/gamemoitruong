from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# NGÂN HÀNG ĐÚNG 100 CÂU HỎI MÔI TRƯỜNG THỰT TẾ
QUESTION_BANK = [
    {"q": "Rác nhựa mất bao lâu để phân hủy hoàn toàn?", "a": ["10 năm", "50 năm", "100-500 năm", "Không bao giờ"], "c": 2},
    {"q": "Loại rác nào sau đây có thể tái chế vô hạn lần?", "a": ["Nhựa", "Giấy", "Thủy tinh", "Xốp"], "c": 2},
    {"q": "Rác hữu cơ (vỏ trái cây, rau củ) nên dùng để làm gì?", "a": ["Đốt", "Làm phân bón", "Vứt xuống cống", "Chôn lấp"], "c": 1},
    {"q": "Pin cũ hết hạn nên xử lý thế nào?", "a": ["Vứt thùng rác", "Đốt", "Gửi điểm thu gom chuyên biệt", "Vứt xuống hồ"], "c": 2},
    {"q": "Nhựa số mấy là nhựa dùng một lần, khó tái chế nhất?", "a": ["Số 1", "Số 2", "Số 5", "Số 7"], "c": 0},
    {"q": "Biểu tượng 3 mũi tên xoay vòng nghĩa là gì?", "a": ["Cấm vứt rác", "Rác nguy hiểm", "Có thể tái chế", "Dễ vỡ"], "c": 2},
    {"q": "Kim loại nào có tỷ lệ tái chế cao nhất?", "a": ["Sắt", "Nhôm", "Đồng", "Vàng"], "c": 1},
    {"q": "Lốp xe cũ thường được tái chế thành gì?", "a": ["Thực phẩm", "Mặt sân cỏ nhân tạo/Giày", "Sách", "Quần áo"], "c": 1},
    {"q": "Ô nhiễm trắng là thuật ngữ chỉ loại ô nhiễm nào?", "a": ["Không khí", "Nguồn nước", "Rác thải nhựa", "Tiếng ồn"], "c": 2},
    {"q": "Vi nhựa thường xâm nhập vào cơ thể người qua đâu?", "a": ["Hơi thở", "Chuỗi thức ăn biển", "Tiếp xúc da", "Ánh sáng"], "c": 1},
    {"q": "Hiện tượng Trái Đất nóng lên do khí nào chủ yếu?", "a": ["Oxy", "Nitơ", "CO2", "Argon"], "c": 2},
    {"q": "Lớp Ozone bảo vệ chúng ta khỏi tia gì?", "a": ["Tia X", "Tia hồng ngoại", "Tia cực tím (UV)", "Tia Gamma"], "c": 2},
    {"q": "Băng tan ở hai cực gây ra hậu quả gì?", "a": ["Biển ngọt hơn", "Nước biển dâng", "Sóng thần", "Động đất"], "c": 1},
    {"q": "Khí Mê-tan (CH4) gây hiệu ứng nhà kính đến từ đâu?", "a": ["Giao thông", "Chăn nuôi gia súc", "Máy tính", "Trồng rừng"], "c": 1},
    {"q": "Hiện tượng El Nino gây ra điều gì?", "a": ["Mưa lớn", "Hạn hán/Nắng nóng", "Bão tuyết", "Lạnh giá"], "c": 1},
    {"q": "Nước nào thải ra nhiều khí nhà kính nhất thế giới?", "a": ["Mỹ", "Trung Quốc", "Việt Nam", "Nga"], "c": 1},
    {"q": "Hiệu ứng nhà kính có tác dụng gì tự nhiên?", "a": ["Làm sạch khí", "Giữ nhiệt cho Trái Đất", "Tạo mưa", "Giảm bụi"], "c": 1},
    {"q": "Mưa axit do khí thải nào gây ra?", "a": ["Oxy", "CO2", "SO2 và NOx", "Nitơ"], "c": 2},
    {"q": "Tầng khí quyển thấp nhất là tầng gì?", "a": ["Tầng đối lưu", "Tầng bình lưu", "Tầng nhiệt", "Tầng ngoài"], "c": 0},
    {"q": "Nghị định thư Kyoto nói về vấn đề gì?", "a": ["Rác nhựa", "Cắt giảm khí nhà kính", "Bảo vệ cá voi", "Trồng rừng"], "c": 1},
    {"q": "Nguồn năng lượng nào là vô tận?", "a": ["Dầu mỏ", "Than đá", "Mặt trời", "Khí đốt"], "c": 2},
    {"q": "Năng lượng địa nhiệt lấy từ đâu?", "a": ["Gió", "Mặt trời", "Lòng đất", "Sóng biển"], "c": 2},
    {"q": "Tiết kiệm điện giúp giảm thải khí gì?", "a": ["CO2", "Oxy", "Nitơ", "Hơi nước"], "c": 0},
    {"q": "Đâu là nhiên liệu hóa thạch?", "a": ["Gió", "Thủy triều", "Than đá", "Địa nhiệt"], "c": 2},
    {"q": "Loại đèn nào ít tốn điện nhất?", "a": ["Đèn dây tóc", "Đèn Halogen", "Đèn LED", "Đèn huỳnh quang"], "c": 2},
    {"q": "Thủy điện lấy năng lượng từ đâu?", "a": ["Nhiệt độ", "Sức chảy của nước", "Gió", "Hóa chất"], "c": 1},
    {"q": "Rừng Amazon được mệnh danh là gì?", "a": ["Kho báu", "Lá phổi xanh Trái Đất", "Vườn quốc gia", "Sa mạc xanh"], "c": 1},
    {"q": "Nguồn nước ngọt trên Trái Đất chiếm bao nhiêu %?", "a": ["97%", "50%", "3%", "70%"], "c": 2},
    {"q": "Năng lượng sinh khối lấy từ đâu?", "a": ["Đá", "Chất thải hữu cơ", "Ánh sáng", "Nam châm"], "c": 1},
    {"q": "Gió được tạo ra do sự chênh lệch về gì?", "a": ["Độ ẩm", "Áp suất không khí", "Độ cao", "Mùi"], "c": 1},
    {"q": "Động vật nào là biểu tượng của WWF?", "a": ["Voi", "Hổ", "Gấu Trúc", "Cá Voi"], "c": 2},
    {"q": "San hô thực chất là gì?", "a": ["Thực vật", "Động vật", "Đá quý", "Rong biển"], "c": 1},
    {"q": "Việc mất rừng gây ra hậu quả gì?", "a": ["Lũ lụt", "Hạn hán", "Mất đa dạng sinh học", "Tất cả các ý trên"], "c": 3},
    {"q": "Loài vật nào có nguy cơ tuyệt chủng do băng tan?", "a": ["Lạc đà", "Gấu Bắc Cực", "Sư tử", "Hươu cao cổ"], "c": 1},
    {"q": "Động vật hoang dã bị săn bắt chủ yếu để làm gì?", "a": ["Lấy gỗ", "Lấy thịt/da/ngà trái phép", "Làm cảnh", "Lấy sữa"], "c": 1},
    {"q": "Ngày Môi trường Thế giới là ngày nào?", "a": ["5/6", "22/4", "1/5", "1/1"], "c": 0},
    {"q": "Giờ Trái Đất diễn ra vào thời gian nào?", "a": ["Tháng 1", "Cuối tháng 3", "Giữa tháng 6", "Tháng 12"], "c": 1},
    {"q": "Hành động nào giúp bảo vệ môi trường nhất?", "a": ["Dùng túi nilon", "Dùng túi vải/giấy", "Đốt rác", "Xả nước lãng phí"], "c": 1},
    {"q": "Phương tiện giao thông nào sạch nhất?", "a": ["Ô tô con", "Xe máy", "Xe đạp", "Máy bay"], "c": 2},
    {"q": "Túi nilon thông thường làm từ đâu?", "a": ["Cây cối", "Dầu mỏ", "Sắt", "Cát"], "c": 1},
    {"q": "Vỏ lon nhôm mất bao lâu để phân hủy?", "a": ["10 năm", "80-100 năm", "200 năm", "500 năm"], "c": 1},
    {"q": "Sản phẩm nào có thể thay thế ống hút nhựa?", "a": ["Ống hút tre", "Ống hút giấy", "Ống hút inox", "Cả 3 phương án trên"], "c": 3},
    {"q": "Nguồn năng lượng nào đến từ sức nóng của Mặt Trời?", "a": ["Thủy điện", "Quang điện", "Địa nhiệt", "Điện gió"], "c": 1},
    {"q": "Hành động '3R' gồm: Reduce, Reuse và ...?", "a": ["Reform", "Recycle", "Remove", "Repeat"], "c": 1},
    {"q": "Loại túi nào thân thiện với môi trường nhất?", "a": ["Túi vải không dệt", "Túi nilon", "Túi nhựa HDPE", "Túi nhựa PVC"], "c": 0},
    {"q": "Việc trồng rừng giúp ngăn chặn điều gì?", "a": ["Lũ quét", "Xói mòn đất", "Sa mạc hóa", "Tất cả các ý trên"], "c": 3},
    {"q": "Nước biển dâng cao đe dọa vùng nào nhất Việt Nam?", "a": ["Đồng bằng sông Hồng", "Miền núi phía Bắc", "Đồng bằng sông Cửu Long", "Tây Nguyên"], "c": 2},
    {"q": "Khí thải từ máy điều hòa nhiệt độ có thể gây hại cho?", "a": ["Tầng Ozone", "Sức khỏe tim mạch", "Thị giác", "Nguồn nước"], "c": 0},
    {"q": "Hạn hán kéo dài dẫn đến hiện tượng gì?", "a": ["Lũ lụt", "Băng tan", "Cháy rừng", "Động đất"], "c": 2},
    {"q": "Loài cá nào đang bị đánh bắt quá mức làm mất cân bằng biển?", "a": ["Cá mập", "Cá voi", "Cá thu", "Cá ngừ"], "c": 0},
    {"q": "Nhựa sinh học được làm từ nguyên liệu gì?", "a": ["Dầu hỏa", "Than đá", "Tinh bột/Xơ thực vật", "Kim loại"], "c": 2},
    {"q": "Việc sử dụng năng lượng hạt nhân có nhược điểm gì?", "a": ["Ít điện", "Giá rẻ", "Rác thải phóng xạ nguy hiểm", "Không khói"], "c": 2},
    {"q": "Ngành công nghiệp nào thải nhiều nước thải nhất?", "a": ["Dệt nhuộm", "Công nghệ thông tin", "Dịch vụ", "Giáo dục"], "c": 0},
    {"q": "Dầu tràn trên biển gây hại gì?", "a": ["Nước biển xanh hơn", "Chết sinh vật biển do thiếu Oxy", "Tăng lượng cá", "Nhanh tan băng"], "c": 1},
    {"q": "Sử dụng phân bón hóa học quá mức gây ô nhiễm?", "a": ["Tiếng ồn", "Đất và nguồn nước ngầm", "Không khí", "Ánh sáng"], "c": 1},
    {"q": "Loài rùa biển nào đang ở mức cực kỳ nguy cấp?", "a": ["Rùa Hoàn Kiếm", "Vích", "Đồi mồi", "Rùa da"], "c": 2},
    {"q": "Tại sao không nên sử dụng hộp xốp đựng thức ăn nóng?", "a": ["Nhanh hỏng", "Thôi nhiễm chất độc vào thức ăn", "Giá đắt", "Gây buồn ngủ"], "c": 1},
    {"q": "Mất bao nhiêu lít nước để sản xuất 1 chiếc quần Jean?", "a": ["10 lít", "100 lít", "1000 lít", "Hơn 7000 lít"], "c": 3},
    {"q": "Phong trào 'Thứ Sáu vì tương lai' nói về điều gì?", "a": ["Vui chơi", "Hành động vì biến đổi khí hậu", "Giảm học", "Trồng cây"], "c": 1},
    {"q": "Chất độc màu da cam gây ảnh hưởng gì lâu dài?", "a": ["Hỏng máy móc", "Dị dạng gen và ô nhiễm đất", "Sóng thần", "Tăng lượng mưa"], "c": 1},
    {"q": "Thứ tự phân loại rác tại nguồn ở Việt Nam hiện nay?", "a": ["Hữu cơ - Tái chế - Còn lại", "Nhựa - Giấy - Sắt", "Độc hại - Thông thường", "Vứt chung"], "c": 0},
    {"q": "Loại rác nào chiếm diện tích lớn nhất tại các bãi rác?", "a": ["Kim loại", "Nhựa và túi nilon", "Thủy tinh", "Gỗ"], "c": 1},
    {"q": "Vi sinh vật có ích trong xử lý rác là?", "a": ["Vi khuẩn gây bệnh", "Nấm men/Vi khuẩn phân hủy", "Virus", "Ký sinh trùng"], "c": 1},
    {"q": "Vật liệu nào sau đây tự nhiên và bền vững?", "a": ["Sợi tổng hợp", "Mây tre đan", "Nhựa PVC", "Polyester"], "c": 1},
    {"q": "Sông Mê Kông chảy qua bao nhiêu quốc gia?", "a": ["3", "4", "6", "10"], "c": 2},
    {"q": "Tác động của thuốc trừ sâu đến ong là gì?", "a": ["Giúp ong khỏe", "Làm ong mất phương hướng và chết hàng loạt", "Tăng mật", "Không ảnh hưởng"], "c": 1},
    {"q": "Rác điện tử (điện thoại, máy tính) chứa chất gì?", "a": ["Vitamin", "Thủy ngân, chì, cadimi", "Chất xơ", "Đường"], "c": 1},
    {"q": "Vành đai lửa Thái Bình Dương nổi tiếng với?", "a": ["Bão cát", "Động đất và núi lửa", "Băng tan", "Nắng nóng"], "c": 1},
    {"q": "Vấn đề nào đe dọa an ninh lương thực toàn cầu?", "a": ["Biến đổi khí hậu", "Dân số tăng quá nhanh", "Mất đất canh tác", "Tất cả các ý trên"], "c": 3},
    {"q": "Đơn vị đo cường độ âm thanh là gì?", "a": ["Hertz", "Watt", "Decibel (dB)", "Volt"], "c": 2},
    {"q": "Ô nhiễm tiếng ồn gây ra điều gì?", "a": ["Hỏng mắt", "Stress và mất ngủ", "Đau chân", "Tăng chiều cao"], "c": 1},
    {"q": "Tầng nào chứa hầu hết các đám mây?", "a": ["Tầng đối lưu", "Tầng bình lưu", "Tầng trung lưu", "Tầng ngoài"], "c": 0},
    {"q": "Màu sắc nào thường dùng cho thùng rác tái chế?", "a": ["Đỏ", "Xanh dương", "Đen", "Vàng"], "c": 1},
    {"q": "Tại sao cần thu gom dầu ăn đã qua sử dụng?", "a": ["Đổ xuống cống gây tắc và ô nhiễm", "Làm sạch bếp", "Để bán rẻ", "Không cần thu gom"], "c": 0},
    {"q": "Lượng rác nhựa thải ra đại dương mỗi năm khoảng?", "a": ["1 triệu tấn", "8 triệu tấn", "100 triệu tấn", "1 tỷ tấn"], "c": 1},
    {"q": "Hành động nào tiêu tốn năng lượng nhất trong nhà?", "a": ["Dùng đèn LED", "Sạc điện thoại", "Dùng bình nóng lạnh/Điều hòa", "Dùng quạt"], "c": 2},
    {"q": "Thủy ngân là kim loại ở thể gì ở nhiệt độ thường?", "a": ["Rắn", "Khí", "Lỏng", "Plasma"], "c": 2},
    {"q": "Rừng ngập mặn có tác dụng gì?", "a": ["Chắn sóng, bảo vệ đê biển", "Nuôi tôm", "Lấy gỗ", "Làm đẹp"], "c": 0},
    {"q": "Chất khí nào chiếm tỉ lệ lớn nhất trong khí quyển?", "a": ["Oxy", "CO2", "Nitơ", "Argon"], "c": 2},
    {"q": "Hiện tượng mù quang hóa thường xảy ra ở đâu?", "a": ["Nông thôn", "Rừng rậm", "Đô thị lớn nhiều khói bụi", "Bãi biển"], "c": 2},
    {"q": "Rác thải y tế thường được xử lý bằng cách?", "a": ["Đổ ra sông", "Hấp khử trùng hoặc thiêu đốt chuyên dụng", "Bán đồng nát", "Chôn lấp chung"], "c": 1},
    {"q": "Sinh vật biến đổi gen (GMO) có thể gây lo ngại về?", "a": ["Mất giống thuần chủng", "Cây nhanh chết", "Quả nhỏ", "Ít nước"], "c": 0},
    {"q": "Vật liệu nào phân hủy nhanh nhất?", "a": ["Túi nilon", "Vỏ chuối", "Vỏ lon nhôm", "Thanh sắt"], "c": 1},
    {"q": "Nguồn phát thải bụi mịn PM2.5 lớn nhất là từ?", "a": ["Nấu ăn", "Giao thông và xây dựng", "Hút thuốc", "Lá cây"], "c": 1},
    {"q": "Tại sao rạn san hô lại được gọi là 'Rừng mưa của biển'?", "a": ["Nhiều mưa", "Đa dạng sinh học cực cao", "Nhiều cây xanh", "Nước ngọt"], "c": 1},
    {"q": "Việc sử dụng lò vi sóng thay lò nướng giúp?", "a": ["Thức ăn ngon hơn", "Tiết kiệm năng lượng", "Đẹp bếp", "Chậm hơn"], "c": 1},
    {"q": "Nguyên nhân chính gây ra triều cường ở TP.HCM?", "a": ["Mưa lớn", "Biến đổi khí hậu dâng nước và sụt lún đất", "Nhiều xe cộ", "Chặt cây"], "c": 1},
    {"q": "Chủ đề của Ngày Trái Đất 2024 là gì?", "a": ["Trồng thêm cây", "Trái Đất và Nhựa (Planet vs. Plastics)", "Tiết kiệm nước", "Yêu thiên nhiên"], "c": 1},
    {"q": "Nghề nào sau đây là 'nghề xanh'?", "a": ["Kỹ sư năng lượng mặt trời", "Sản xuất nhựa", "Khai thác than", "Lái máy bay"], "c": 0},
    {"q": "Vải sợi tự nhiên làm từ gì?", "a": ["Nhựa", "Bông, lanh, tơ tằm", "Than đá", "Sắt"], "c": 1},
    {"q": "Bảo tồn nội vi (In-situ) là bảo tồn tại?", "a": ["Sở thú", "Môi trường tự nhiên của chúng", "Phòng thí nghiệm", "Công viên"], "c": 1},
    {"q": "Rác vô cơ gồm những gì?", "a": ["Thức ăn thừa", "Gạch, đá, sành sứ", "Lá cây", "Xác động vật"], "c": 1},
    {"q": "Sự cố hạt nhân Chernobyl xảy ra ở quốc gia nào?", "a": ["Mỹ", "Nhật Bản", "Ukraine (Liên Xô cũ)", "Đức"], "c": 2},
    {"q": "Sản phẩm OCOP của Việt Nam khuyến khích?", "a": ["Dùng đồ nhập khẩu", "Khai thác tài nguyên bản địa bền vững", "Dùng nhiều nhựa", "Sản xuất công nghiệp nặng"], "c": 1},
    {"q": "Công nghệ Nano trong môi trường giúp?", "a": ["Tăng rác", "Xử lý nước và lọc khí hiệu quả", "Gây ô nhiễm", "Làm đẹp"], "c": 1},
    {"q": "Đơn vị đo lượng phát thải Carbon?", "a": ["Kg", "Lít", "Tấn CO2 tương đương", "Mét khối"], "c": 2},
    {"q": "Tác động của du lịch đại trà là gì?", "a": ["Tăng thu nhập", "Hủy hoại cảnh quan và xả rác quá tải", "Giảm bụi", "Làm sạch biển"], "c": 1},
    {"q": "Phát triển bền vững là phát triển cho?", "a": ["Chỉ người giàu", "Thế hệ hiện tại và tương lai", "Chỉ động vật", "Ngành nhựa"], "c": 1},
    {"q": "Bạn có thể đóng góp bảo vệ môi trường bằng cách?", "a": ["Học tập kiến thức xanh", "Lan tỏa ý thức cho người thân", "Thực hành phân loại rác", "Tất cả các ý trên"], "c": 3}
]

leaderboard = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_questions')
def get_questions():
    # Bốc ngẫu nhiên 20 câu trong kho 100 câu thật cho mỗi trận
    selected = random.sample(QUESTION_BANK, 20)
    return jsonify({"questions": selected})

@app.route('/submit_score', methods=['POST'])
def submit_score():
    data = request.json
    leaderboard.append({"name": data['name'], "score": data['score'], "time": data['time']})
    leaderboard.sort(key=lambda x: (-x['score'], x['time']))
    return jsonify({"leaderboard": leaderboard[:10]})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
