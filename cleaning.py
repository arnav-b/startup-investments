"""
Clean up the objects and acquisitions datasets.
"""
import numpy as np
import pandas as pd 

def clean_objects(filename, nrows=500):
    objects = pd.read_csv(filename, nrows=nrows)
    objects = objects[objects["entity_type"] == "Company"]
    objects = objects.dropna(subset=["name", "category_code"]).reset_index()
    return objects

def clean_acquisitions(filename, objects, nrows=500):
    acquisitions = pd.read_csv(filename, nrows=nrows)
    acquisitions = acquisitions.dropna().reset_index()
    objects_ids = set(objects["id"])
    todrop = []
    for idx in range(len(acquisitions)):
        if acquisitions.loc[idx, "acquiring_object_id"] not in objects_ids or \
            acquisitions.loc[idx, "acquired_object_id"] not in objects_ids:
            todrop.append(idx)
    acquisitions = acquisitions.drop(labels=todrop)
    return acquisitions

def main():
    objects = clean_objects("data/objects.csv")
    acquisitions = clean_acquisitions("data/acquisitions.csv", objects)
    print(objects.shape)
    print(acquisitions.shape)
    objects.to_csv("objects_cleaned.csv")
    acquisitions.to_csv("acquisitions_cleaned.csv")

if __name__ == "__main__":
    main()