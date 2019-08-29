# -*- coding: utf-8 -*-
import pandas as pd 
import networkx as nx
 
df = pd.read_csv("data-challenge.csv", index_col=0)
print ('original dataset shape: ', df.shape)

df = df[~df.duplicated()]
print ('unduplicated dataset shape: ',df.shape)

df1 = df.reset_index().groupby(["d_r_uuid", "license_id"], as_index=False).first()
print ("count of each license: ", '\n', "license_id ", "count")
print (df1['license_id'].value_counts())

print("Number of license under 1 version of each software")
df1 = df.reset_index().groupby(["d_r_uuid", "version"]).size().sort_values(ascending=False)
print (df1)
print("# of lisense", "count")
print(df1.value_counts())

print("percentage of software that use each dependency")
print(df.iloc[:,0:3].stack().value_counts(normalize=True)) #delete normalize=True to return frequency of each dependency instead of %
print("frequency", "count")
print(df.iloc[:,0:3].stack().value_counts().value_counts())

df = df.reset_index()
# combine all versions
df.drop(["license_id", "version"], axis=1, inplace=True) 
df = pd.melt(df, id_vars="d_r_uuid", value_name="dependency")
# or treat each version seperately
#df.drop("license_id", axis=1, inplace=True) 
#df = pd.melt(df, id_vars=["d_r_uuid", "version"], value_name="dependency")
G = nx.from_pandas_dataframe(df, "d_r_uuid", "dependency", edge_attr=True, create_using=nx.DiGraph())

#write graph 
nx.write_graphml(G,"dependency.graphml")

