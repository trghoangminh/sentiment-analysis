import csv
import random
import os

def generate_vietnamese_sarcasm():
    print("Đang khởi tạo máy nhân bản Dữ liệu Châm biếm (Data Augmentation)...")
    
    # 1. Từ vựng cơ bản
    objects = ["Điện thoại", "Laptop", "Tai nghe", "Áo", "Quần", "Ví", "Giày", "Sản phẩm", "Món này", "Đồ ăn", "Quán cà phê", "Nhà hàng", "Dịch vụ", "Phim này", "Camera", "Bàn phím", "Màn hình", "Nước hoa", "Son"]
    
    pos_looks = ["thiết kế quá đẹp", "bóng bẩy", "nhìn sang trọng", "bao bì bắt mắt", "đẹp lộng lẫy", "đẹp mê ly", "nhìn xịn xò", "bề ngoài xuất sắc"]
    neg_looks = ["hơi xấu", "xấu tệ", "cồng kềnh", "phèn phèn", "quê mùa", "không đẹp", "nhìn rẻ tiền", "nhìn như đồ chợ", "ngoại hình xấu xí"]
    
    pos_func = ["xài siêu mượt", "bền vô đối", "ổn áp phết", "cực kỳ tiện dụng", "chất lượng tuyệt vời", "ngon nghẻ", "10 điểm", "chất lượng đỉnh cao", "đẹp xuất sắc bên trong"]
    neg_func = ["như hạch", "xài 3 bữa là hỏng", "vứt xó", "như đồ chơi trẻ con", "chán chẳng buồn nói", "phí tiền", "vô dụng", "tệ hại", "ứa gan"]

    wait_times = ["2 tiếng", "nửa ngày", "1 tuần", "mòn mỏi", "ròng rã 3 tiếng", "dài cả cổ"]
    fake_compliments = ["best dịch vụ", "xuất sắc nhất hệ mặt trời", "tuyệt vời nhất trần đời", "100 sao cho sự chậm trễ", "làm ăn quá chuyên nghiệp (cười)"]

    dataset = []

    # Bẫy 1: Xấu bề ngoài nhưng Tốt bên trong -> Tích cực (2)
    for _ in range(1500):
        o = random.choice(objects)
        n = random.choice(neg_looks)
        p = random.choice(pos_func)
        patterns = [
            f"{o} {n} nhưng {p}.",
            f"Mặc dù {o.lower()} {n} nhưng thật sự {p}.",
            f"Tuy {n} nhưng {o.lower()} này {p}.",
            f"Bề ngoài {n} thế thôi chứ {p} nha.",
            f"{o} nhìn thì {n} đấy, cơ mà {p}."
        ]
        dataset.append((random.choice(patterns), 2))

    # Bẫy 2: Đẹp bề ngoài nhưng Tệ bên trong -> Tiêu cực (0)
    for _ in range(1500):
        o = random.choice(objects)
        p = random.choice(pos_looks)
        n = random.choice(neg_func)
        patterns = [
            f"{o} {p} nhưng {n}.",
            f"Chỉ được cái {p} chứ xài thì {n}.",
            f"Mua vì {p} mà ai dè {n}.",
            f"{o} mã thì {p} đấy nhưng bên trong mục nát {n}.",
            f"Khen cho cố {p} vào rồi mua về {n}."
        ]
        dataset.append((random.choice(patterns), 0))

    # Bẫy 3: Giao hàng chậm/Dịch vụ tệ + Khen đểu (Sarcasm) -> Tiêu cực (0)
    for _ in range(1000):
        w = random.choice(wait_times)
        f = random.choice(fake_compliments)
        patterns = [
            f"Bắt để khách đợi {w}, {f}!",
            f"Wow, giao hàng mất đúng {w}, {f}.",
            f"Quá tuyệt vời, chỉ cần đợi {w} là có hàng, {f}.",
            f"Chăm sóc khách hàng quá tốt, gọi điện để mình nghe nhạc chờ {w}, {f}."
        ]
        dataset.append((random.choice(patterns), 0))

    # Bẫy 4: Khen ngợi tuyệt đối với từ lóng (Slang) -> Tích cực (2)
    slangs = ["đỉnh chóp", "hết nước chấm", "mười điểm không có nhưng", "chuẩn không cần chỉnh", "mua đi không hối hận", "đáng đồng tiền bát gạo"]
    for _ in range(1000):
        o = random.choice(objects)
        s = random.choice(slangs)
        dataset.append((f"{o} này đúng là {s}!", 2))
        dataset.append((f"Thề, {o.lower()} {s}.", 2))

    # Bẫy 5: Chê thậm tệ -> Tiêu cực (0)
    heavy_negs = ["cạch mặt tới già", "làm ăn chộp giật", "treo đầu dê bán thịt chó", "nhắn tin không thèm rep", "toàn bọn lừa đảo"]
    for _ in range(1000):
        o = random.choice(objects)
        h = random.choice(heavy_negs)
        dataset.append((f"Bán {o.lower()} kiểu đấy thì {h}.", 0))
        dataset.append((f"{o} mua về bị lỗi, shop {h}.", 0))
        
    random.shuffle(dataset)
    
    # Ghi ra tệp CSV
    output_path = "data/processed/sarcasm_dataset.csv"
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["text", "label"])
        for text, label in dataset:
            writer.writerow([text, label])
            
    print(f"✅ Đã tạo thành công {len(dataset)} dòng dữ liệu bẫy cực hiểm vào {output_path}!")

if __name__ == "__main__":
    generate_vietnamese_sarcasm()
