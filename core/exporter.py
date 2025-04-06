import csv

class DataExporter:
    @staticmethod
    def to_csv(data, filename):
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write header
                writer.writerow(['Field', 'Value'])
                
                # Write basic info
                writer.writerow(['Name', data.get('name', '')])
                writer.writerow(['Headline', data.get('headline', '')])
                writer.writerow(['About', data.get('about', '')])
                writer.writerow(['Profile URL', data.get('url', '')])
                
                # Write experience
                writer.writerow([])
                writer.writerow(['Experience'])
                for exp in data.get('experience', []):
                    writer.writerow(['Title', exp.get('title', '')])
                    writer.writerow(['Company', exp.get('company', '')])
                    writer.writerow(['Duration', exp.get('duration', '')])
                    writer.writerow([])
                
            return True
        except Exception as e:
            print(f"Export error: {str(e)}")
            return False