import os
import requests
import json

apiID = os.environ['acID']
apiToken = os.environ['acToken']
apiURL = 'https://www.redcap-cats.org/promis_api/'


def ac_api_call(method):
    r = requests.post(apiURL + method, auth=(apiID, apiToken))
    r = json.loads(r.text)
    return r


def build_item_bank(form, location):
    x = ac_api_call('/2014-01/Forms/' + form['FormID'] + '.json')
    y = ac_api_call('/2014-01/Calibrations/' + form['FormID'] + '.json')
    d = dict()
    for i in range(0, len(y['Properties'])):
        for k, v in y['Properties'][i].items():
            d[k] = v
    d['Items'] = dict()
    for i in range(0, len(x['Items'])):
        d['Items'][i] = dict()
        f_form_item_oid = x['Items'][i]['FormItemOID']
        d['Items'][i]['ID'] = x['Items'][i]['ID']
        for q in range(0, len(y['Items'])):
            c_form_item_oid = y['Items'][q]['FormItemOID']
            if c_form_item_oid == f_form_item_oid:
                d['Items'][i]['A_GRM'] = y['Items'][q]['A_GRM']
                for j in range(0, len(x["Items"][i]['Elements'])):
                    d['Items'][i]['Responses'] = dict()
                    d['Items'][i]['betas'] = list()
                    element_description = x['Items'][i]['Elements'][j]['Description']
                    if j == 0:
                        if element_description[:18] == 'In the past 7 days':
                            desc1 = x['Items'][i]['Elements'][j]['Description']
                            desc2 = x['Items'][i]['Elements'][j + 1]['Description']
                            d['Items'][i]['Description'] = desc1 + ', ' + desc2
                        else:
                            d['Items'][i]['Description'] = x['Items'][i]['Elements'][j]['Description']
                    if j + 1 == len(x["Items"][i]['Elements']):
                        for k in range(0, len(x['Items'][i]['Elements'][j]['Map'])):
                            d['Items'][i]['Responses'][k] = dict()
                            f_item_resp_oid = x['Items'][i]['Elements'][j]['Map'][k]['ItemResponseOID']
                            d['Items'][i]['Responses'][k]['Difficulty'] = x['Items'][i]['Elements'][j]['Map'][k]['Value']
                            desc = x['Items'][i]['Elements'][j]['Map'][k]['Description']
                            d['Items'][i]['Responses'][k]['Description'] = desc
                            # d['Items'][i]['Responses'][k]['Position'] = x['Items'][i]['Elements'][j]['Map'][k]['Position']
                            for r in range(0, len(y['Items'][q]['Map'])):
                                c_item_resp_oid = y['Items'][q]['Map'][r]['ItemResponseOID']
                                if c_item_resp_oid == f_item_resp_oid:
                                    # d['Items'][i]['Responses'][k]['StepOrder'] = y['Items'][q]['Map'][r]['StepOrder']
                                    #
                                    #
                                    # TODO: Need to check whether I'm reversing the order or not...
                                    d['Items'][i]['betas'].insert(0, y['Items'][q]['Map'][r]['Threshold'])
    with open(location + form['FormID'] + '.json', 'w') as outfile:
        json.dump(d, outfile)

formName = {'Form': 'PROMIS PHYSICAL FUNCTION V1.2', 'FormID': '56296D2D-C919-40F1-AFC7-6F544FCA7772'}
build_item_bank(formName, 'Assessments/')

formName = {'Form': 'PROMIS Bank v1.0 - Anxiety', 'FormID': 'FFCDF6E3-8B17-4673-AB38-C677FFF6DBAF'}
build_item_bank(formName, 'Assessments/')
