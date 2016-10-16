using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using System.Text;
using System.IO;

public class LoadInText : MonoBehaviour {

    public string[] filenames;
    public GameObject lungTissue;
    public GameObject targetTissue;

    private int lungTissueObjectsGenerated;

    public float[] thresholds;
    public Color[] correspondingColours;

    // Use this for initialization  
    void Awake() {
        lungTissueObjectsGenerated = 0;
        //Load(filename);
        foreach (string filename in filenames)
        {
            Load(filename);
        }
    }

    private bool Load(string fileName)
    {
        // Handle any problems that might arise when reading the text
        try
        {
            string line;
            // Create a new StreamReader, tell it which file to read and what encoding the file
            // was saved as
            StreamReader theReader = new StreamReader(fileName, Encoding.Default);
            // Immediately clean up the reader after this block of code is done.
            // You generally use the "using" statement for potentially memory-intensive objects
            // instead of relying on garbage collection.
            // (Do not confuse this with the using directive for namespace at the 
            // beginning of a class!)
            List<GameObject> tissueObjectsCreated = new List<GameObject>();
            using (theReader)
            {
                // While there's lines left in the text file, do this:     
                do
                {
                    line = theReader.ReadLine();

                    if (line != null)
                    {
                        string[] entries = line.Split(',');

                        float x = 0;
                        float y = 0;
                        float z = 0;
                        float radiationVal = 0;

                        int counter = 0;
                        foreach (string entry in entries)
                        {
                            if (counter == 0)
                            {
                                x = float.Parse(entry);
                            }

                            if (counter == 1)
                            {
                                y = float.Parse(entry);
                            }

                            if (counter == 2)
                            {
                                z = float.Parse(entry);
                            }

                            if (counter == 3)
                            {
                                radiationVal = float.Parse(entry);
                            }

                            counter++;
                        }
                        if (fileName.Contains("Target"))
                        {
                            tissueObjectsCreated.Add((GameObject)Instantiate(targetTissue, new Vector3(x, y, z), Quaternion.identity));
                            Color color = new Color(255, 255, 255);
                            for (int i = 0; i < thresholds.Length; i++)
                            {
                                if (radiationVal < thresholds[i])
                                {
                                    color = correspondingColours[i];
                                    break;
                                }
                            }
                            tissueObjectsCreated[tissueObjectsCreated.Count - 1].GetComponent<Renderer>().material.color = color;

                        }
                        else
                        {
                            tissueObjectsCreated.Add((GameObject)Instantiate(lungTissue, new Vector3(x, y, z), Quaternion.identity));
                            Color color = new Color(255, 255, 255);
                            for (int i = 0; i < thresholds.Length; i++)
                            {
                                if (radiationVal < thresholds[i])
                                {
                                    color = correspondingColours[i];
                                    break;
                                }
                            }
                            tissueObjectsCreated[tissueObjectsCreated.Count - 1].GetComponent<Renderer>().material.color = color;

                        }

                    }
                }
                while (line != null);
                // Done reading, close the reader and return true to broadcast success    
                theReader.Close();

                //for all tissueObjects
                //ray trace and find matching

                //List<GameObject> hitGameObjects = new List<GameObject>(); //don't visit these again

                //foreach (GameObject tissueObject in tissueObjectsCreated)
                //{
                //    if (hitGameObjects.Contains(tissueObject) == false)
                //    {
                //        //ray trace left
                //        RaycastHit hit;
                //        GameObject hitObject;
                //        if (Physics.Raycast(new Ray(tissueObject.transform.position, new Vector3(-1, 0, 0)), out hit))
                //        {
                //            hitObject = hit.collider.gameObject;
                //            if (tissueObjectsCreated.Contains(hitObject)) //if it's a part of this organ
                //            {
                //                hitGameObjects.Add(hitObject);
                //                for (int i = 1; i < (tissueObject.transform.position - hitObject.transform.position).magnitude; i+=2)
                //                {
                //                    if (fileName.Contains("Target"))
                //                        Instantiate(targetTissue, tissueObject.transform.position - new Vector3(i, 0, 0), Quaternion.identity);
                //                    else
                //                        Instantiate(lungTissue, tissueObject.transform.position - new Vector3(i, 0, 0), Quaternion.identity);

                //                }
                //            }
                //        }

                //        //ray trace right
                //        if (Physics.Raycast(new Ray(tissueObject.transform.position, new Vector3(1, 0, 0)), out hit))
                //        {

                //            hitObject = hit.collider.gameObject;
                //            if (tissueObjectsCreated.Contains(hitObject))
                //            {
                //                hitGameObjects.Add(hitObject);
                //                for (int i = 1; i < (tissueObject.transform.position - hitObject.transform.position).magnitude; i+=2)
                //                {
                //                    if (fileName.Contains("Target"))
                //                        Instantiate(targetTissue, tissueObject.transform.position + new Vector3(i, 0, 0), Quaternion.identity);
                //                    else
                //                        Instantiate(lungTissue, tissueObject.transform.position + new Vector3(i, 0, 0), Quaternion.identity);

                //                }
                //            }
                //        }
                //    }
                //}
                
                return true;
            }
        }
        //// If anything broke in the try block, we throw an exception with information
        //// on what didn't work
        catch (System.Exception e)
        {
            //Debug.Log("Error!");
            Debug.Log(e.Message);
            //Debug.Log("{0}\n", e.Message);
            return false;
        }
    }

        
}

