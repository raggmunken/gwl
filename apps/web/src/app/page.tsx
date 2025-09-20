import { redirect } from "next/navigation";

export default function Home() {
  // Redirect root to Swedish locale by default
  redirect("/sv");
}
