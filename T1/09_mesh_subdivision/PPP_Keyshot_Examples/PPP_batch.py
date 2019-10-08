# -*- coding: utf-8 -*-
# AUTHOR Dries Vervoort (Luxion)
# VERSION 0.0.1
# Batch render OBJ models to images.
import os, re #Import modules os (operating system dependent functionality) and re (regular expression matching operations)

#Function to do a sanity check on the dialog options.
def checkDialogOptions(opts, importExtension):
  #Condition: "ifold" is empty (length = 0).
  if len(opts["ifold"]) == 0:
    #Script stops with error and shows exception in "Show Output".
    raise Exception("Import folder cannot be empty! Please specify a folder.")
  #Condition: "ofold" is empty (length = 0).
  if len(opts["ofold"]) == 0:
    #Script stops with error and shows exception in "Show Output".
    raise Exception("Output folder cannot be empty! Please specify a folder.")
  #Condition: "samples" is empty (length = 0).
  if opts["samples"] == 0:
    #Script stops with error and shows exception in "Show Output".
    raise Exception("Invalid render option!")

  patternExtension = ".*{}".format(importExtension)
  found = False
  #For all files in the import folder...
  for file in os.listdir(opts["ifold"]):
    #Condition: ".step" matches file in import folder.
    if re.match(patternExtension, file):
      found = True
      #Break out of the for loop.
      break
  #Condition: found = False.
  if not found:
    #Script stops with error and shows exception in "Show Output". No files with extension "step" (importExtension) in import folder.
    raise Exception("Could not find any OBJ files in \"{}\"!".format(opts["ifold"]))

#Function to set the right import options for STEP models.
def getGeometryImportOptions():
  importOptions = lux.getImportOptions()
  importOptions['center_geometry'] = True
  importOptions['snap_to_ground'] = True
  #Set "Up Orientation" for import to "Z".
  importOptions['up_vector'] = 1
  importOptions['adjust_camera_look_at'] = False
  importOptions['adjust_environment'] = False
  importOptions['update_mode'] = False
  importOptions['group_by_shader'] = False
  # importOptions['retain_materials'] = True
  #A value of '2' for group_by equals GroupByObject. The model is structured with grouping by objects.
  importOptions['group_by'] = 2
  importOptions['new_import'] = False
  importOptions['tessellation_quality'] = 0.15
  importOptions['accurate_tessellation'] = True
  #Return dictionary importOptions to main() function.
  return importOptions

#Function to set the Render Options and Lighting Preset.
def setRenderOptions(samples, lightingPreset, queue):
  #Get dictionary of render options.
  renderOptions = lux.getRenderOptions()
  #If queue = True ("Add to queue" checked in dialog) then a job will be added to the KeyShot Queue instead of being rendered immediately.
  renderOptions.setAddToQueue(queue)
  #Set "Maximum Samples" quality with amount of samples specified in dialog.
  renderOptions.setMaxSamplesRendering(samples)
  #Return dictionary renderOptions to main() function.
  return renderOptions

#Function to get the cameras in the scene.
def getCameras(allCameras):
  #Condition: "Render all eras" is checked in dialog.
  if allCameras:
    #Put the cameras in the scene in a list. [0:-1] to exclude the 'default' camera.
    cameraToRender = lux.getCameras()[1:]

  #Condition: "Render all cameras" is not checked in dialog.
  else:
    #Get the active camera and put it in a list.
    cameraToRender = [lux.getCamera()]
  #Return list cameraToRender to main() function.
  return cameraToRender

#Function to set the render height based on render width, by keeping the realtime ratio.
def aspectRatio(sceneInfo, imageWidth):
  sceneWidth = sceneInfo.get('width')
  sceneHeight = sceneInfo.get('height')
  ratioHeightWidth = sceneHeight / sceneWidth
  imageHeight = int(imageWidth * ratioHeightWidth)
  #Return integer imageHeight to main() function.
  return imageHeight

#Function to render images or create render jobs.
def renderImage(cameraToRender, outputFolder, file, style, outputExtension, imageWidth, imageHeight, renderOptions):
  #Loop for all cameras in list cameraToRender.
  for camera in cameraToRender:
    #Set the current camera.
    lux.setCamera(camera)
    outputPath = outputFolder + os.path.sep + file
    outputPath = os.path.splitext(outputPath)[0] + "_" + style + "_" + str(camera) + "." + str(outputExtension)
    print("Rendering {}".format(outputPath))
    if not lux.renderImage(path = outputPath, width = imageWidth, height = imageHeight, opts = renderOptions):
      print("Rendering was cancelled by user.")
      break

#Main function
def main():
  tmpls = ["-- None --"] + lux.getMaterialTemplates()
  sceneInfo = lux.getSceneInfo()
  #Create a list with image formats as strings.
  imageFormatCombo = ["jpeg", "png", "tiff", "exr"]
  #Get list of lighting presets.
  lightingPresetCombo = lux.getLightingPresets()
  #Adds "Currently used" to the end of list lightingPresetCombo.
  lightingPresetCombo.append('Currently used')
            #Model import folder. "None" can be replaced with a folder path, so that the script always starts with that value. It can save time for not having to browse to the model folder.
  values = [("ifold", lux.DIALOG_FOLDER, "Folder to import OBJ models from:", None),
            (lux.DIALOG_LABEL, "--"),
            ("oext", lux.DIALOG_ITEM, "Output image format:", "png", imageFormatCombo),
            #Image output folder. "None" can be replaced with a folder path, so that the script always starts with that value. It can save time for not having to browse to the output folder.
            ("ofold", lux.DIALOG_FOLDER, "Output folder:", None),
            (lux.DIALOG_LABEL, "--"),
            (lux.DIALOG_LABEL, "Render settings:"),
            ("preset", lux.DIALOG_ITEM, "Lighting preset to use:", lightingPresetCombo[-1], lightingPresetCombo),
            ("camera", lux.DIALOG_CHECK, "Render all cameras", True),
            ("width", lux.DIALOG_INTEGER, "Render width:", sceneInfo.get('width'), (1, 10000)),
            ("height", lux.DIALOG_INTEGER, "Render height:", sceneInfo.get('height'), (1, 10000)),
            ("ratio", lux.DIALOG_CHECK, "Keep realtime aspect ratio (Use only width)", True),
            ("samples", lux.DIALOG_INTEGER, "Maximum samples:", 64),
            (lux.DIALOG_LABEL, "--"),
            ("template", lux.DIALOG_ITEM, "Apply material template on each import (optional):",tmpls[0], tmpls),
            (lux.DIALOG_LABEL, "--")]
            # (lux.DIALOG_LABEL, "Options:"),
            # ("queue", lux.DIALOG_CHECK, "Add to queue", True),
            # ("process", lux.DIALOG_CHECK, "Process queue after running script", False)]
                            #Show dialog according to the arguments provided and return the results. title = Title of the dialog.
  opts = lux.getInputDialog(title = "Batch Render Model Collection",
                            #desc = Description of dialog.
                            desc = "Renders a collection of models in a folder to images.",
                            #values = The values of the dialog to build and show. It expects a list of tuples, one tuple for each control.
                            values = values,
                            #id = ID that enables persisting values. Values will be remembered when clicking OK and will be default values when reopening. Make sure that the ID is unique to the script!
                            id = "batchrenderOBJmodels.py.luxion")
  if not opts: return

  #Set STEP as the model format to import.
  importExtension = "obj"

  #Call function to do a sanity check on the dialog options. (Find function above main())
  checkDialogOptions(opts, importExtension)

  #Assign "ifold" dialog value to variable importFolder.
  importFolder = opts["ifold"]
  #Assign dialog value "oext" (selected from combobox) to variable outputExtension. [1] accesses value at index 1 in list imageFormatCombo.
  outputExtension = opts["oext"][1]
  #Assign "ofold" dialog value to variable outputFolder.
  outputFolder = opts["ofold"]
  #Assign "toon" dialog value to variable toonPass.
  #Assign dialog value "preset" (selected from combobox) to variable lightingPreset. [1] accesses value at index 1 in list lightingPresetCombo.
  lightingPreset = opts["preset"][1]
  #Assign "camera" dialog value to variable allCameras.
  allCameras = opts["camera"]
  #Assign "width" dialog value to variable imageWidth.
  imageWidth = opts["width"]
  #Assign "height" dialog value to variable imageHeight.
  imageHeight = opts["height"]
  #Assign "ratio" dialog value to variable realtimeRatio.
  realtimeRatio = opts["ratio"]
  #Assign "samples" dialog value to variable samples.
  samples = opts["samples"]
  #Assign "queue" dialog value to variable queue.
  # queue = opts["queue"]
  queue = False
  #Assign "process" dialog value to variable process.
  # process = opts["process"]
  process = False
  template = opts["template"]

  if template[0] == 0:
      template = None
  else:
      template = template[1]

  #Call function to set the appropriate import options. (Find function above main())
  importOptions = getGeometryImportOptions()
  #Call function to set selected Render Options and Lighting Preset. (Find function above main())
  renderOptions = setRenderOptions(samples, lightingPreset, queue)
  #Call function to get the cameras in the scene. (Find function above main())
  cameraToRender = getCameras(allCameras)

  #Condition: "Keep realtime aspect ratio (Use only width)" is checked in dialog.
  if realtimeRatio:
    #Function to set the render height based on render width, by keeping the realtime ratio. (Find function above main())
    imageHeight = aspectRatio(sceneInfo, imageWidth)

  #Create new empty list
  modelList = []
  #Loop for all files in folder "importFolder".
  for file in os.listdir(importFolder):
    #Condition: file ends with extension "importExtension" ("step").
    if file.endswith(importExtension):
      #Add file string to end of list modelList.
      modelList.append(file)
      #Print the list. This list is only intended to provide information.
      print(modelList)

      #Get file path of scene.
      scenePath = sceneInfo.get('file')
      #Reload scene.
      lux.openFile(scenePath)

      #Condition: "Lighting preset to use:" in dialog doesn't equal "Currently used".
      if lightingPreset != 'Currently used':
        #Set selected lighting preset.
        lux.setLightingPreset(lightingPreset)

      #Full path to the file of the model to import.
      importPath = importFolder + os.path.sep + file

      print("Importing {}".format(importPath))
      #Import model in scene.
      if not lux.importFile(path = importPath, opts = importOptions):
        #Script stops with error and shows exception in "Show Output" if the import is interrupted.
        raise Exception("Error in import! User cancelled?")

      #Apply material template for "Realistic" style to scene.
      lux.setMaterialTemplate(template)
      style = "PPP"
      #Call function to render images and pass the necessary arguments. (Find function above main())
      renderImage(cameraToRender, outputFolder, file, style, outputExtension, imageWidth, imageHeight, renderOptions)


  #Condition: "Process queue after running script" is checked in dialog.
  if process:
    print("Processing queue")
    #Process Queue to render jobs.
    lux.processQueue()

#Call main function.
main()
