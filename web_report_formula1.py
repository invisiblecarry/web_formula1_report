from flask import Flask, render_template, request
from formula1.report import parse_log_files, load_abbreviations, build_report, print_report
import os

app = Flask(__name__)
app.config['DATA_FOLDER'] = os.path.join('', 'data')


def get_report():
    start_data = parse_log_files(app.config['DATA_FOLDER'], "start.log")
    end_data = parse_log_files(app.config['DATA_FOLDER'], "end.log")
    abbreviations = load_abbreviations(app.config['DATA_FOLDER'], "abbreviations.txt")
    report = build_report(start_data, end_data, abbreviations)
    return report


@app.route('/report/')
def show_report():
    report = get_report()
    order = request.args.get('order', 'asc')
    sorted_report = sorted(report.items(), key=lambda x: x[1]['Best Lap Time'])
    if order == 'desc':
        sorted_report.reverse()
    return render_template('report.html', report=sorted_report)


@app.route('/report/drivers/')
def show_driver_list():
    report = get_report()
    order = request.args.get('order', 'asc')
    sorted_report = sorted(report.items(), key=lambda x: x[1]['Best Lap Time'])
    if order == 'desc':
        sorted_report.reverse()
    driver_ids = {item[0]: report[item[0]]['Abbreviation'] for item in sorted_report}
    return render_template('driver_list.html', driver_ids=driver_ids)


@app.route('/report/drivers/info/')
def show_driver_info():
    report = get_report()
    driver_id = request.args.get('driver_id')
    driver_info = [value for key, value in report.items() if report[key]['Abbreviation'] == driver_id]
    if len(driver_info) > 0:
        return render_template('driver_info.html', driver_info=driver_info)
    else:
        return "Driver not found"


if __name__ == '__main__':
    app.run(debug=True)
