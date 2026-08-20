import time
import requests

WEBHOOK_URL = "https://webhook.site/bfd5d8c0-55a2-434a-a854-5b1d2508e0b4"
TARGET_URL = "https://hackerone.com" # Или любой другой сайт для теста

def fetch_and_parse_site():
    print(f"[*] Скачиваем данные с сайта: {TARGET_URL}")
    start_time = time.time()
    
    try:
        response = requests.get(TARGET_URL, timeout=10)
        duration = time.time() - start_time
        
        # Собираем базовую информацию
        report = {
            "status": "SITE_FETCH_SUCCESS",
            "target_url": TARGET_URL,
            "http_status_code": response.status_code,
            "response_time_sec": round(duration, 4),
            "content_size_bytes": len(response.content),
            "headers_sample": dict(list(response.headers.items())[:5]), # Первые 5 заголовков ответа
            "json_data": response.json() if "application/json" in response.headers.get("Content-Type", "") else "Not JSON"
        }
        
        print(f"[+] Успешно! Статус: {response.status_code}, Время: {duration:.4f} сек.")
        return report

    except Exception as e:
        print(f"[-] Ошибка при запросе сайта: {e}")
        return {
            "status": "SITE_FETCH_ERROR",
            "error_message": str(e)
        }

if __name__ == "__main__":
    print("🚀 Запуск простого и надежного воркера в раннере...")
    
    # Получаем данные
    report_payload = fetch_and_parse_site()
    
    # Отправляем результаты на Webhook
    print("[*] Отправка результатов на Webhook...")
    try:
        webhook_response = requests.post(WEBHOOK_URL, json=report_payload, timeout=10)
        print(f"[+] Отчет успешно доставлен! Статус webhook: {webhook_response.status_code}")
    except Exception as e:
        print(f"[-] Ошибка отправки на Webhook: {e}")
