import os
import instaloader
import glob

def instaScraper():
    L = instaloader.Instaloader(save_metadata=False)

    # List of usernames
    usernames = ['vogueindia','fashionfloorindia','thesouledstore', '__ranbir_kapoor_official__', 'stylebyami', 'watchingnewyork']  # Add the usernames you want to download posts from
    # Loop through the usernames
    for username in usernames:
        try:
            # Load a profile
            profile = instaloader.Profile.from_username(L.context, username)
            print("Got profile")
            count =0 
            # Get the first two posts from the profile
            for post in profile.get_posts():
                # Download the post
                if not post.is_video:
                    L.download_post(post, target="posts")
                    count+=1
                    if count==2:
                        break
        except Exception as e:
            print(f"An error occurred with user {username}: {e}")
    txt_files = glob.glob(os.path.join("posts", '*.txt'))
    for txt_file in txt_files:
        os.remove(txt_file)

if __name__ == "__main__":
    instaScraper()