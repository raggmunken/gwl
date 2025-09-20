import {createClient} from "next-sanity";
import {projectId, dataset, apiVersion, useCdn} from "@/sanity/config";

export const sanityClient = createClient({
  projectId,
  dataset,
  apiVersion,
  useCdn,
});

export function getPreviewClient() {
  const token = process.env.SANITY_API_TOKEN;
  return createClient({
    projectId,
    dataset,
    apiVersion,
    useCdn: false,
    token,
    perspective: token ? "previewDrafts" : "published",
  });
}
