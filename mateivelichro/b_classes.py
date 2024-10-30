import requests
import pandas

#this class aprses a json. It is used to parse API responses
class req_json():
    #example of optional arguments
    def __init__(self, endpoint, payload=None, header=None):     
        
        def get_response():

            response=requests.get(self.endpoint, params=self.payload, headers=self.headers)
            status_code=response.status_code

            if status_code==200:
                json_response=response.json()
            else:
                json_response={}
            
            return status_code, response, json_response
                
                
        self.headers=header
        self.payload=payload
        self.endpoint=endpoint
        get_response_retun=get_response()
        self.status_code=get_response_retun[0]
        self.response=get_response_retun[1]
        self.json_response=get_response_retun[2]

# This class is tailored to read my predefined models and manipualte the data
# It creates a dataframe, pivots it, calculates totals etc.
# After all that it reads total consumption per each topic and creates specia attributes so that I can easily and safely pass them to the CanvasJS function
class req_sqlite():
        def __init__(self, model_source, key_source):     
             
            def parse_dict(dict_val):
                out_col=[]
                for  key, value in dict_val.items():
                    out_col.append({ "label":key,"y":value})
                return out_col    
                
                    
            self.model_source=model_source
            self.key_source=key_source
            self.p_df=pandas.DataFrame(list(model_source)).merge(pandas.DataFrame(list(key_source)),on='item_name', how='inner', suffixes=('_1', '_2'))
            self.p_df['Total_CO2'] = self.p_df['quantity'].astype(int) * self.p_df['item_co2perunit'].astype(int)
            self.pivot_df=self.p_df.pivot_table(index='month', columns='item_name', aggfunc='sum')['Total_CO2']
            self.dict_data=self.pivot_df.to_dict()
            self.LPG=parse_dict(self.dict_data['LPG'])
            self.Gasoline=parse_dict(self.dict_data['Gasoline'])
            self.Elec_ap8=parse_dict(self.dict_data['Elec_ap8'])
            self.Elec_ap20=parse_dict(self.dict_data['Elec_ap20'])
            self.Gas_ap8=parse_dict(self.dict_data['Gas_ap8'])
            self.Gas_ap20=parse_dict(self.dict_data['Gas_ap20'])
            self.Work_flight=parse_dict(self.dict_data['Work_flight'])
            self.Leisure_flight=parse_dict(self.dict_data['Leisure_flight'])