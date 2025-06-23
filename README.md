## Repository Tổng Hợp Tài Liệu và Dự Án An Ninh Mạng

Repository này được tạo ra để lưu trữ các tài liệu học tập, bài thực hành Lab, và các dự án liên quan đến môn học An ninh mạng (NT140) tại Đại học Công nghệ Thông tin (VNU-HCM). Mục tiêu là cung cấp một cái nhìn tổng quan về kiến thức và kinh nghiệm thực tế trong lĩnh vực này, đặc biệt tập trung vào khả năng bảo vệ và ứng phó với các mối đe dọa không gian mạng.

---

## 1. Thư mục: `lab`

Thư mục này chứa các bài thực hành và tài liệu liên quan đến các buổi Lab của môn An ninh mạng. Các bài Lab bao gồm:

* Web Application Firewall
* Improving Mod Security WAF
* Database Security
* Security with Snyk in DevSecOps
* Building a network monitoring system with PfSense and Splunk
* DDoS attack

Các lab 1, 2, 4, 5 được báo cáo trực tiếp tại lớp

Các lab 3 và 6 được viết thành báo cáo

---

## 2. Thư mục: `project`

### Dự án: Advanced malware protection

Dự án này tập trung vào việc thiết kế và triển khai một hệ thống tự động để phân tích mã độc động, tích hợp với thông tin tình báo mối đe dọa (Threat Intelligence) và khả năng chặn bắt lưu lượng mạng thời gian thực, nhằm nâng cao khả năng phát hiện và phân tích phần mềm độc hại.

### Thành phần chính của hệ thống

* **Client (Hệ điều hành Ubuntu)**: Máy người dùng thực hiện yêu cầu tải file từ Internet.
* **Cuckoo Agent (Máy ảo Windows 10)**: Được cấu hình trong VirtualBox, đóng vai trò là môi trường cách ly để chạy và phân tích hành vi của mã độc. Được cấu hình để truy cập Internet thông qua proxy.
* **MISP (Malware Information Sharing Platform)**: Hệ thống thông tin chia sẻ mối đe dọa, đóng vai trò là cơ sở dữ liệu Threat Intelligence.
* **API tích hợp**:
    * **VirusTotal API**: Cung cấp dịch vụ phân tích file dựa trên cơ sở dữ liệu lớn.
    * **Nessus API**: Cung cấp dịch vụ quét và đánh giá lỗ hổng bảo mật.
    * **Cuckoo API**: Giao tiếp với Cuckoo Sandbox để gửi yêu cầu phân tích và nhận báo cáo kết quả.
* **MITMProxy**: Proxy trung gian được sử dụng để giám sát, chặn bắt và phân tích lưu lượng mạng ra/vào.
* **Script Python**: Đảm nhận vai trò điều phối chính: xử lý và tổng hợp báo cáo từ các nguồn (VirusTotal API, Cuckoo API, Nessus), gửi yêu cầu đến OpenAI để tạo báo cáo cuối cùng và đề xuất khắc phục (remediation).

### Luồng hoạt động của hệ thống

1.  **Quét ban đầu**: Nessus thực hiện quét lỗ hổng trên Cuckoo Agent (máy ảo Windows 10) *trước khi* bất kỳ mã độc nào được chạy, nhằm ghi nhận trạng thái ban đầu của hệ thống.
2.  **Yêu cầu tải file**: Client (máy Ubuntu) gửi yêu cầu tải xuống một file bất kỳ từ Internet.
3.  **Chặn bắt bởi Proxy**: File được chặn lại tại MITMProxy để kiểm tra ban đầu.
4.  **Kiểm tra Threat Intelligence (MISP)**: Hệ thống kiểm tra hàm băm (hash) của file đó có tồn tại trong cơ sở dữ liệu MISP và có được đánh dấu là độc hại không.
    * Nếu **có hash trong MISP và được đánh dấu độc hại**: Quá trình tải xuống sẽ bị từ chối ngay lập tức.
    * Nếu **hash không có trong MISP (hoặc chưa xác định)**: File sẽ được chuyển tiếp (forward) vào Cuckoo Sandbox để chạy và phân tích trong môi trường Cuckoo Agent (máy ảo Windows 10).
5.  **Phân tích tại Cuckoo Sandbox**: Cuckoo Sandbox tiến hành chạy và phân tích hành vi của file. Sau khi hoàn tất, nó sẽ gửi một báo cáo phản hồi ngắn gọn về cho proxy.
6.  **Kiểm tra kết quả Cuckoo**: Nếu báo cáo từ Cuckoo cho thấy file là độc hại, quá trình tải file về Client (Ubuntu) sẽ bị từ chối.
7.  **Tổng hợp báo cáo từ VirusTotal**: Một script Python sẽ sử dụng hash của file để lấy báo cáo chi tiết từ VirusTotal API.
8.  **Tổng hợp báo cáo từ Cuckoo**: Sau khi Cuckoo phân tích xong, nó sẽ gửi báo cáo đầy đủ thông qua Cuckoo API đến script Python tổng hợp.
9.  **Quét sau lây nhiễm (Nessus)**: Sau khi gửi báo cáo từ Cuckoo, Cuckoo sẽ gọi đến Nessus để thực hiện quét lỗ hổng trên Cuckoo Agent (máy ảo Windows 10) *sau khi* mã độc đã chạy.
10. **Tổng hợp báo cáo Nessus**: Sau khi Nessus hoàn tất quét, nó sẽ gửi báo cáo kết quả đến script Python tổng hợp.
11. **Tạo báo cáo cuối cùng bằng OpenAI**: Script Python, sau khi nhận được đầy đủ các báo cáo từ VirusTotal, Cuckoo và Nessus, sẽ gửi một yêu cầu đến OpenAI. OpenAI sẽ tổng hợp toàn bộ dữ liệu này và tạo ra một báo cáo cuối cùng cùng với các đề xuất khắc phục (remediation).

### Kết quả của thực nghiệm: [**Remediation**](https://github.com/PNNhatTram/NT140---Network-Security/blob/main/Project/remediation.html)
