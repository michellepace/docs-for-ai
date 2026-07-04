# Build a fullstack app with Next.js 16 and Prisma Postgres

**Author:** Lee Robinson

---

Build a fullstack blog with the Next.js 16 App Router, Prisma, Sign in with Vercel, and Prisma Postgres from the Vercel Marketplace. The app starts with hardcoded content, then adds a managed Postgres database, Vercel account authentication, Server Actions, drafts, publishing, and deployment to Vercel.

## Prerequisites

To follow this tutorial, you need:

- Node.js 20.19 or later
  
- A Vercel account
  
- A GitHub account
  
- npm, which is included with Node.js
  

## Step 1: Create the starter app

Create a Next.js 16 project from the starter repository:

`npx create-next-app --example https://github.com/prisma/blogr-nextjs-prisma/tree/main blogr-nextjs-prisma`

Move into the project and start the development server:

`cd blogr-nextjs-prisma npm run dev`

Open `http://localhost:3000`. The starter app uses the App Router and renders a hardcoded blog feed from `lib/posts.ts`.

The starter uses these files:

- `app/layout.tsx`: The root layout and navigation
  
- `app/page.tsx`: The public feed page
  
- `app/posts/[id]/page.tsx`: The post detail page    - `components/post-card.tsx`: The post preview component    - `lib/posts.ts`: Temporary hardcoded post data    You will replace the hardcoded data with Prisma Postgres and Prisma ORM in the next steps. ## Step 2: Create a Prisma Postgres database Use [Prisma Postgres](https://vercel.com/marketplace/prisma), a serverless Postgres provider in the Vercel Marketplace, as the database for this app.

First, create a GitHub repository for your project and push the starter code:

`git init git add . git commit -m "init" git branch -M main git remote add origin git@github.com:YOUR_GITHUB_USERNAME/blogr-nextjs-prisma.git git push -u origin main`

Then create a Vercel project from that repository. After the project exists, open the **Storage** tab in the Vercel dashboard and select the **Connect Database** button. Choose **Prisma** from the Marketplace providers.

Connect the database to the Vercel project. The Prisma integration adds a database environment variable to the project:

- `DATABASE_URL`: The connection string for application queries
  

For Prisma schema commands, you can optionally set `DIRECT_URL` to a direct connection string copied from Prisma Console. If `DIRECT_URL` is not set, this guide falls back to `DATABASE_URL`.

Install the Vercel CLI and pull the Vercel project environment variables into your local project:

`npm i -g vercel@latest vercel env pull .env`

Your local `.env` file now contains the database connection strings that Prisma and the app will use.

## Step 3: Install Prisma and configure Prisma Postgres

Install Prisma, Prisma Client, the `pg` adapter for Prisma, and `dotenv`:

`npm install @prisma/client @prisma/adapter-pg dotenv npm install prisma --save-dev`

Add a `postinstall` script to `package.json` so Prisma Client is generated during installs and Vercel builds:

`{ "scripts": { "dev": "next dev", "build": "next build", "start": "next start", "postinstall": "prisma generate" } }`

Create a `prisma` directory and add `prisma/schema.prisma`:

`generator client { provider = "prisma-client" output = "../generated/prisma" } datasource db { provider = "postgresql" } model Post { id String @id @default(cuid()) title String content String? published Boolean @default(false) author User? @relation(fields: [authorId], references: [id]) authorId String? } model User { id String @id @default(cuid()) vercelId String @unique @map("vercel_id") name String? email String? @unique image String? createdAt DateTime @default(now()) @map(name: "created_at") updatedAt DateTime @updatedAt @map(name: "updated_at") posts Post[] @@map(name: "users") }` Prisma 7 configures database connection strings in `prisma.config.ts` instead of the `datasource` block. Create `prisma.config.ts` in the project root: `import "dotenv/config"; import { defineConfig } from "prisma/config"; export default defineConfig({ schema: "prisma/schema.prisma", datasource: { url: process.env.DIRECT_URL ?? process.env.DATABASE_URL ?? "", }, });` The Prisma CLI uses `DIRECT_URL` when you provide it because schema commands should use a direct database connection. The application uses `DATABASE_URL` through the Prisma `pg` adapter. Update `.gitignore` so the generated Prisma Client is not committed: `generated/prisma/` Push the schema to Prisma Postgres and generate Prisma Client: `npx prisma db push npx prisma generate` Create `lib/prisma.ts` to instantiate Prisma Client with the Prisma `pg` adapter: `import { PrismaPg } from "@prisma/adapter-pg"; import { PrismaClient } from "@/generated/prisma/client"; const connectionString = process.env.DATABASE_URL; if (!connectionString) { throw new Error("DATABASE_URL is not set"); } const adapter = new PrismaPg({ connectionString }); const globalForPrisma = globalThis as unknown as { prisma?: PrismaClient; }; const prisma = globalForPrisma.prisma ?? new PrismaClient({ adapter }); if (process.env.NODE_ENV !== "production") { globalForPrisma.prisma = prisma; } export default prisma;` ## Step 4: Load posts from the database Replace the hardcoded feed with a Prisma query. Update `components/post-card.tsx`: ``import Link from "next/link"; import ReactMarkdown from "react-markdown"; export type PostCardData = { id: string; title: string; content: string | null; author: { name: string | null; } | null; }; export default function PostCard({ post }: { post: PostCardData }) { return ( <Link className="post-card" href={`/posts/${post.id}`}> <h2>{post.title}</h2> <p className="meta">By {post.author?.name ?? "Unknown author"}</p> {post.content ? <ReactMarkdown>{post.content}</ReactMarkdown> : null} </Link> ); }`` Update `app/page.tsx`: `import PostCard, { type PostCardData } from "@/components/post-card"; import prisma from "@/lib/prisma"; export const revalidate = 10; export default async function FeedPage() { const feed = await prisma.post.findMany({ where: { published: true }, include: { author: { select: { name: true }, }, }, orderBy: { id: "desc" }, }); return ( <div className="stack"> <h1>Public Feed</h1> {feed.length ? ( feed.map((post: PostCardData) => <PostCard key={post.id} post={post} />) ) : ( <div className="panel">No published posts yet.</div> )} </div> ); }` Update `app/posts/[id]/page.tsx`: ``import { notFound } from "next/navigation"; import ReactMarkdown from "react-markdown"; import prisma from "@/lib/prisma"; type PostPageProps = { params: Promise<{ id: string }>; }; export default async function PostPage({ params }: PostPageProps) { const { id } = await params; const post = await prisma.post.findUnique({ where: { id }, include: { author: { select: { name: true }, }, }, }); if (!post) { notFound(); } const title = post.published ? post.title : `${post.title} (Draft)`; return ( <article className="panel"> <h1>{title}</h1> <p className="meta">By {post.author?.name ?? "Unknown author"}</p> {post.content ? <ReactMarkdown>{post.content}</ReactMarkdown> : null} </article> ); }`` You can add sample data in Prisma Studio: `npx prisma studio` Create a `User` with a placeholder `vercelId`, such as `demo-user`, then create a published `Post` and connect it to that user. Refresh `http://localhost:3000` to see the database-backed feed. ## Step 5: Add Sign in with Vercel [Sign in with Vercel](https://vercel.com/docs/sign-in-with-vercel) lets users authenticate with their Vercel account. The app will redirect users to Vercel's authorization endpoint, exchange the returned code for tokens, verify the ID Token, and store the access token in an HTTP-only cookie.

Install `jose` to verify the ID Token signature:

`npm install jose`

Create a Sign in with Vercel App in the Vercel dashboard:

1. Open your team's **Settings** page.
   
2. Select **Apps**.
   
3. Select the **Create** button.
   
4. Enter an app name and slug.
   
5. Select the **Save** button.
   
6. Generate a client secret.
   
7. Add `http://localhost:3000/api/auth/callback` to **Authorization Callback URLs**.
   
8. Enable the `openid`, `email`, and `profile` scopes in **Permissions**.
   

Add the App credentials to `.env`:

`NEXT_PUBLIC_VERCEL_APP_CLIENT_ID="your_vercel_app_client_id_here" VERCEL_APP_CLIENT_SECRET="your_vercel_app_client_secret_here"`

Create `app/api/auth/authorize/route.ts` to start the OAuth flow:

``import crypto from "node:crypto"; import { cookies } from "next/headers"; import { type NextRequest, NextResponse } from "next/server"; function generateSecureRandomString() { return crypto.randomBytes(32).toString("base64url"); } function getClientId() { const clientId = process.env.NEXT_PUBLIC_VERCEL_APP_CLIENT_ID; if (!clientId) { throw new Error("NEXT_PUBLIC_VERCEL_APP_CLIENT_ID is not set"); } return clientId; } export async function GET(request: NextRequest) { const state = generateSecureRandomString(); const nonce = generateSecureRandomString(); const codeVerifier = generateSecureRandomString(); const codeChallenge = crypto .createHash("sha256") .update(codeVerifier) .digest("base64url"); const cookieStore = await cookies(); const secure = process.env.NODE_ENV === "production"; cookieStore.set("oauth_state", state, { httpOnly: true, maxAge: 10 * 60, path: "/", sameSite: "lax", secure, }); cookieStore.set("oauth_nonce", nonce, { httpOnly: true, maxAge: 10 * 60, path: "/", sameSite: "lax", secure, }); cookieStore.set("oauth_code_verifier", codeVerifier, { httpOnly: true, maxAge: 10 * 60, path: "/", sameSite: "lax", secure, }); const params = new URLSearchParams({ client_id: getClientId(), code_challenge: codeChallenge, code_challenge_method: "S256", nonce, redirect_uri: `${request.nextUrl.origin}/api/auth/callback`, response_type: "code", scope: "openid email profile", state, }); return NextResponse.redirect( `https://vercel.com/oauth/authorize?${params.toString()}`, ); }``

Create `app/api/auth/callback/route.ts` to exchange the authorization code for tokens and sync the Vercel user into Prisma Postgres:

``import { createRemoteJWKSet, jwtVerify, type JWTPayload } from "jose"; import { cookies } from "next/headers"; import { type NextRequest, NextResponse } from "next/server"; import prisma from "@/lib/prisma"; const jwks = createRemoteJWKSet(new URL("https://vercel.com/.well-known/jwks")); type TokenData = { access_token: string; expires_in: number; id_token: string; scope: string; token_type: string; }; type VercelIdToken = JWTPayload & { email?: string; name?: string; nonce?: string; picture?: string; preferred_username?: string; sub: string; }; function getClientId() { const clientId = process.env.NEXT_PUBLIC_VERCEL_APP_CLIENT_ID; if (!clientId) { throw new Error("NEXT_PUBLIC_VERCEL_APP_CLIENT_ID is not set"); } return clientId; } function getClientSecret() { const clientSecret = process.env.VERCEL_APP_CLIENT_SECRET; if (!clientSecret) { throw new Error("VERCEL_APP_CLIENT_SECRET is not set"); } return clientSecret; } function validate(value: string | null | undefined, storedValue?: string) { return Boolean(value && storedValue && value === storedValue); } async function exchangeCodeForToken( code: string, codeVerifier: string, requestOrigin: string, ) { const response = await fetch("https://api.vercel.com/login/oauth/token", { method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded", }, body: new URLSearchParams({ client_id: getClientId(), client_secret: getClientSecret(), code, code_verifier: codeVerifier, grant_type: "authorization_code", redirect_uri: `${requestOrigin}/api/auth/callback`, }), }); if (!response.ok) { throw new Error("Failed to exchange authorization code for token"); } return (await response.json()) as TokenData; } async function verifyIdToken(idToken: string) { const { payload } = await jwtVerify(idToken, jwks, { audience: getClientId(), issuer: "https://vercel.com", }); if (!payload.sub) { throw new Error("ID token is missing subject"); } return payload as VercelIdToken; } async function syncUser(payload: VercelIdToken) { await prisma.user.upsert({ where: { vercelId: payload.sub }, update: { email: payload.email, name: payload.name ?? payload.preferred_username, image: payload.picture, }, create: { vercelId: payload.sub, email: payload.email, name: payload.name ?? payload.preferred_username, image: payload.picture, }, }); } export async function GET(request: NextRequest) { try { const code = request.nextUrl.searchParams.get("code"); const state = request.nextUrl.searchParams.get("state"); const storedState = request.cookies.get("oauth_state")?.value; const storedNonce = request.cookies.get("oauth_nonce")?.value; const codeVerifier = request.cookies.get("oauth_code_verifier")?.value; if (!code || !codeVerifier) { throw new Error("Authorization code and verifier are required"); } if (!validate(state, storedState)) { throw new Error("State mismatch"); } const tokenData = await exchangeCodeForToken( code, codeVerifier, request.nextUrl.origin, ); const idToken = await verifyIdToken(tokenData.id_token); if (!validate(idToken.nonce, storedNonce)) { throw new Error("Nonce mismatch"); } await syncUser(idToken); const cookieStore = await cookies(); const secure = process.env.NODE_ENV === "production"; cookieStore.set("access_token", tokenData.access_token, { httpOnly: true, maxAge: tokenData.expires_in, path: "/", sameSite: "lax", secure, }); cookieStore.set("oauth_state", "", { maxAge: 0, path: "/" }); cookieStore.set("oauth_nonce", "", { maxAge: 0, path: "/" }); cookieStore.set("oauth_code_verifier", "", { maxAge: 0, path: "/" }); return NextResponse.redirect(new URL("/", request.url)); } catch (error) { console.error("OAuth callback error:", error); return NextResponse.redirect(new URL("/auth/error", request.url)); } }``

Create `lib/auth.ts` to read the access token cookie, request Vercel user info, and return the matching database user:

``import { cookies } from "next/headers"; import prisma from "@/lib/prisma"; type VercelUserInfo = { sub: string; email?: string; name?: string; preferred_username?: string; picture?: string; }; export async function getCurrentUser() { const cookieStore = await cookies(); const accessToken = cookieStore.get("access_token")?.value; if (!accessToken) { return null; } const response = await fetch("https://api.vercel.com/login/oauth/userinfo", { headers: { Authorization: `Bearer ${accessToken}`, }, cache: "no-store", }); if (!response.ok) { return null; } const userInfo = (await response.json()) as VercelUserInfo; if (!userInfo.sub) { return null; } return prisma.user.upsert({ where: { vercelId: userInfo.sub }, update: { email: userInfo.email, name: userInfo.name ?? userInfo.preferred_username, image: userInfo.picture, }, create: { vercelId: userInfo.sub, email: userInfo.email, name: userInfo.name ?? userInfo.preferred_username, image: userInfo.picture, }, }); }``

Create `app/api/auth/signout/route.ts` to revoke the access token and clear the cookie:

``import { cookies } from "next/headers"; import { type NextRequest, NextResponse } from "next/server"; export async function POST(request: NextRequest) { const cookieStore = await cookies(); const accessToken = cookieStore.get("access_token")?.value; if (accessToken) { const credentials = `${process.env.NEXT_PUBLIC_VERCEL_APP_CLIENT_ID}:${process.env.VERCEL_APP_CLIENT_SECRET}`; await fetch("https://api.vercel.com/login/oauth/token/revoke", { method: "POST", headers: { Authorization: `Basic ${Buffer.from(credentials).toString("base64")}`, "Content-Type": "application/x-www-form-urlencoded", }, body: new URLSearchParams({ token: accessToken }), }); } cookieStore.set("access_token", "", { maxAge: 0, path: "/" }); return NextResponse.redirect(new URL("/", request.url), { status: 303 }); }``

Create `app/auth/error/page.tsx` for failed sign-in attempts:

`import Link from "next/link"; export default function AuthErrorPage() { return ( <div className="panel"> <h1>Authentication error</h1> <p>Sign in could not be completed. Try signing in again.</p> <Link className="button" href="/api/auth/authorize"> Sign in with Vercel </Link> </div> ); }`

Update `app/layout.tsx` to show login, logout, draft, and new post controls:

`import type { Metadata } from "next"; import Link from "next/link"; import { getCurrentUser } from "@/lib/auth"; import "./globals.css"; export const metadata: Metadata = { title: "Blogr", description: "A fullstack blog built with Next.js, Prisma, Sign in with Vercel, and Prisma Postgres.", }; export default async function RootLayout({ children, }: Readonly<{ children: React.ReactNode; }>) { const user = await getCurrentUser(); return ( <html lang="en"> <body> <header className="header"> <nav className="nav" aria-label="Main navigation"> <Link href="/">Feed</Link> {user ? <Link href="/drafts">My drafts</Link> : null} </nav> <div className="header-actions"> {user ? ( <> <span className="user">{user.name ?? user.email}</span> <Link className="button secondary" href="/create"> New post </Link> <form action="/api/auth/signout" method="post"> <button type="submit">Log out</button> </form> </> ) : ( <Link className="button" href="/api/auth/authorize"> Sign in with Vercel </Link> )} </div> </header> <main>{children}</main> </body> </html> ); }`

Restart the development server and select the **Sign in with Vercel** button. After Vercel redirects back to the app, the callback route creates or updates the user record in Prisma Postgres through Prisma.

## Step 6: Add Server Actions for posts

Server Actions let your forms mutate data without creating separate API Route files.

Create `app/actions.ts`:

``"use server"; import { revalidatePath } from "next/cache"; import { redirect } from "next/navigation"; import { getCurrentUser } from "@/lib/auth"; import prisma from "@/lib/prisma"; export async function createPost(formData: FormData) { const user = await getCurrentUser(); if (!user) { redirect("/api/auth/authorize"); } const title = String(formData.get("title") ?? "").trim(); const content = String(formData.get("content") ?? "").trim(); if (!title || !content) { throw new Error("Title and content are required."); } await prisma.post.create({ data: { title, content, author: { connect: { id: user.id } }, }, }); revalidatePath("/drafts"); redirect("/drafts"); } export async function publishPost(id: string) { const user = await getCurrentUser(); if (!user) { redirect("/api/auth/authorize"); } const post = await prisma.post.findUnique({ where: { id }, select: { authorId: true }, }); if (post?.authorId !== user.id) { throw new Error("You can only publish your own posts."); } await prisma.post.update({ where: { id }, data: { published: true }, }); revalidatePath("/"); revalidatePath(`/posts/${id}`); revalidatePath("/drafts"); redirect("/"); } export async function deletePost(id: string) { const user = await getCurrentUser(); if (!user) { redirect("/api/auth/authorize"); } const post = await prisma.post.findUnique({ where: { id }, select: { authorId: true }, }); if (post?.authorId !== user.id) { throw new Error("You can only delete your own posts."); } await prisma.post.delete({ where: { id } }); revalidatePath("/"); revalidatePath("/drafts"); redirect("/"); }``

Create `app/create/page.tsx`:

`import Link from "next/link"; import { createPost } from "@/app/actions"; import { getCurrentUser } from "@/lib/auth"; export default async function CreatePage() { const user = await getCurrentUser(); if (!user) { return ( <div className="panel"> <h1>New Draft</h1> <p>You need to be authenticated to create a post.</p> </div> ); } return ( <div className="panel"> <form action={createPost} className="form"> <h1>New Draft</h1> <label className="field"> <span>Title</span> <input autoFocus name="title" placeholder="Title" required /> </label> <label className="field"> <span>Content</span> <textarea name="content" placeholder="Content" required /> </label> <div className="actions"> <button type="submit">Create</button> <Link className="button secondary" href="/"> Cancel </Link> </div> </form> </div> ); }`

Create `app/drafts/page.tsx`:

`import PostCard, { type PostCardData } from "@/components/post-card"; import { getCurrentUser } from "@/lib/auth"; import prisma from "@/lib/prisma"; export default async function DraftsPage() { const user = await getCurrentUser(); if (!user) { return ( <div className="panel"> <h1>My Drafts</h1> <p>You need to be authenticated to view this page.</p> </div> ); } const drafts = await prisma.post.findMany({ where: { authorId: user.id, published: false, }, include: { author: { select: { name: true }, }, }, orderBy: { id: "desc" }, }); return ( <div className="stack"> <h1>My Drafts</h1> {drafts.length ? ( drafts.map((post: PostCardData) => <PostCard key={post.id} post={post} />) ) : ( <div className="panel">You do not have any drafts yet.</div> )} </div> ); }`

Update `app/posts/[id]/page.tsx` so authors can publish and delete their posts: ``import { notFound } from "next/navigation"; import ReactMarkdown from "react-markdown"; import { deletePost, publishPost } from "@/app/actions"; import { getCurrentUser } from "@/lib/auth"; import prisma from "@/lib/prisma"; type PostPageProps = { params: Promise<{ id: string }>; }; export default async function PostPage({ params }: PostPageProps) { const { id } = await params; const [user, post] = await Promise.all([ getCurrentUser(), prisma.post.findUnique({ where: { id }, include: { author: { select: { name: true, email: true }, }, }, }), ]); if (!post) { notFound(); } const postBelongsToUser = user?.id === post.authorId; const title = post.published ? post.title : `${post.title} (Draft)`; return ( <article className="panel"> <h1>{title}</h1> <p className="meta">By {post.author?.name ?? "Unknown author"}</p> <ReactMarkdown>{post.content}</ReactMarkdown> {postBelongsToUser ? ( <div className="actions"> {!post.published ? ( <form action={publishPost.bind(null, post.id)}> <button type="submit">Publish</button> </form> ) : null} <form action={deletePost.bind(null, post.id)}> <button className="secondary" type="submit"> Delete </button> </form> </div> ) : null} </article> ); }`` Add the form and button styles to `app/globals.css`: `button, input, textarea { font: inherit; } button, .button { border: 1px solid var(--foreground); border-radius: 6px; background: var(--foreground); color: var(--surface); cursor: pointer; display: inline-flex; padding: 0.6rem 0.9rem; } button.secondary, .button.secondary { background: transparent; color: var(--foreground); } .header-actions { align-items: center; display: flex; gap: 0.75rem; margin-left: auto; } .user { color: var(--muted); font-size: 0.875rem; } .actions { display: flex; gap: 0.75rem; margin-top: 1.5rem; } .form { display: grid; gap: 1rem; } .field { display: grid; gap: 0.4rem; } .field span { font-weight: 600; } input, textarea { border: 1px solid var(--border); border-radius: 8px; padding: 0.75rem; width: 100%; } textarea { min-height: 180px; resize: vertical; }` Restart the development server, sign in with Vercel, create a draft, publish it, and delete it. ## Step 7: Deploy to Vercel Before deploying, add your production callback URL to the Sign in with Vercel App in the Vercel dashboard: `https://YOUR_VERCEL_PROJECT.vercel.app/api/auth/callback` In the Vercel dashboard, confirm that your project has these environment variables: - `DATABASE_URL`    - `DIRECT_URL` (optional, for Prisma schema commands)    - `NEXT_PUBLIC_VERCEL_APP_CLIENT_ID`    - `VERCEL_APP_CLIENT_SECRET`    If you connected Prisma Postgres from the **Storage** tab, Vercel adds `DATABASE_URL` for you. Add the Sign in with Vercel variables from the App's **Manage** page before deploying. If you use a direct connection string from Prisma Console, add it as `DIRECT_URL`. Commit and push your changes: `git add . git commit -m "build fullstack blog" git push` Create a deployment from the Vercel dashboard or with the Vercel CLI: `vercel deploy` After the deployment completes, open the production URL and test the Sign in with Vercel flow. ## Conclusion You built and deployed a fullstack blog with Next.js 16, the App Router, Prisma, Sign in with Vercel, Prisma Postgres, and Vercel. The final example app is available in the [\`final\`](https://github.com/prisma/blogr-nextjs-prisma/tree/final) branch of the example repository.

---

[View full KB sitemap](/kb/sitemap.md)
