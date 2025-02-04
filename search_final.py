from DEWPython.DEWModel import DEW

# Create DEW model instance to access the species list
model = DEW()

# Print all aqueous species that contain "acetate" or "acetic"
print("All available species containing 'acetate' or 'acetic':")
for name in model.nameLst:
    if 'acetate' in name.lower() or 'acetic' in name.lower():
        print(name)