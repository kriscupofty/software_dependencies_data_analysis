# -*- coding: utf-8 -*-
import pandas as pd 
import networkx as nx
 
df = pd.read_csv("data-challenge.csv", index_col=0)
print ('original dataset shape: ', df.shape)

df1 = df.reset_index().groupby(["d_r_uuid", "license_id"], as_index=False).first()
print ("count of each license: ", '\n', "license_id ", "count")
print (df1['license_id'].value_counts())

print("Number of license under each software")
df1 = df1.groupby("d_r_uuid").size().sort_values(ascending=False)
print (df1)
print("# of lisense", "count")
print(df1.value_counts())


df = df[~df.index.duplicated(keep='first')]  
#use df = df.groupby(["d_r_uuid", "version"]).first() if distinguishing same software of different versions
print ('unduplicated dataset shape: ',df.shape)

print("percentage of software that use each dependency")
print(df.iloc[:,0:3].stack().value_counts(normalize=True)) #delete normalize=True to return frequency of each dependency instead of %
print("frequency", "count")
print(df.iloc[:,0:3].stack().value_counts().value_counts())

df = df.reset_index()
df.drop(["license_id", "version"], axis=1, inplace=True) 
df = pd.melt(df, id_vars="d_r_uuid", value_name="dependency")
#if there are significant differences between different versions, replace the above 2 lines by
#df.drop("version", axis=1, inplace=True) 
#df = pd.melt(df, id_vars=["d_r_uuid", "version"], value_name="dependency")
G = nx.from_pandas_dataframe(df, "d_r_uuid", "dependency", edge_attr=True, create_using=nx.DiGraph())
#nx.draw(G)

#write graph 
nx.write_graphml(G,"dependency.graphml")

