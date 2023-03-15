from github import Github
from social_django.models import UserSocialAuth
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from slugify import slugify

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def get_access_token(user):
    return UserSocialAuth.objects.get(user=user).extra_data['access_token']

def get_user_repositories(user):
    access_token = get_access_token(user)
    if access_token:
        g = Github(access_token)
        print(g.get_user().get_repos().totalCount)
        repositories = list()
        for r in g.get_user().get_repos(): 
            if r.allow_forking:
                try:
                    internal_repository = GitRepository.objects.get(
                        user=user,
                        github_id=r.id
                    )
                    internal_id = internal_repository.id
                except:
                    internal_id = None

                issues = list()
                for i in r.get_issues():
                    try:
                        internal_issue = GitIssue.objects.get(
                            user=user,
                            github_id=i.id
                        )
                        internal_id = internal_issue.id
                        lamports = internal_issue.lamports
                        minimum_date = internal_issue.minimum_date
                        is_active = internal_issue.is_active
                        pda = internal_issue.pda

                        issues.append({'state':i.state,'github_issue_id':i.id,'github_issue_number':i.number,'title': i.title, 'body':i.body, 'github_repository_id':r.id,'internal_issue_id':internal_id,'lamports':lamports,'minimum_date':minimum_date, 'pda':pda ,'is_active':is_active})
                    except:
                        issues.append({'state':i.state,'github_issue_id':i.id,'github_issue_number':i.number,'title': i.title, 'body':i.body, 'github_repository_id':r.id})

                repositories.append({'github_repository_id': r.id, 'name': r.name, 'internal_repository_id':internal_id, 'issues':issues})
        return repositories
    return []

def get_open_issues(user, repository):
    access_token = get_access_token(user)
    if access_token:
        g = Github(access_token)
        repository = g.get_repo(repository)
        issues = list()
        for i in repository.get_issues():
            try:
                internal_issue = GitIssue.objects.get(
                    user=user,
                    github_id=i.id
                )
                internal_id = internal_issue.id
                lamports = internal_issue.lamports
                minimum_date = internal_issue.minimum_date
                is_active = internal_issue.is_active
                pda = internal_issue.pda

                issues.append({'state':i.state,'github_issue_id':i.id,'github_issue_number':i.number,'title': i.title, 'body':i.body, 'github_repository_id':repository.id,'internal_issue_id':internal_id,'lamports':lamports,'minimum_date':minimum_date, 'pda':pda ,'is_active':is_active})
            except:
                issues.append({'state':i.state,'github_issue_id':i.id,'github_issue_number':i.number,'title': i.title, 'body':i.body, 'github_repository_id':repository.id})

    
        return issues
    return []

def create_issue(user, data):
    '''
    Parameters:

    repository = required
    lamports = required

    issue_number = optional (will Link issue instead of creating if in parameters)

    title = optional
    body = optional

    '''

    access_token = get_access_token(user)
    if access_token:
        g = Github(access_token)
        repository = g.get_repo(user.username + '/' + data['repository'])
        repository_obj, ctd = GitRepository.objects.get_or_create(
            user=user,
            github_id=repository.id
        )
        repository_obj.name = repository.name
        repository_obj.save()

        try:
            config = {
                "url": "https://a8ea-69-157-240-115.ngrok.io/github/webhook",
                "content_type": "json"
            }
            EVENTS = ['*']
            repository.create_hook("web", config, EVENTS, active=True)
        except:
            pass

        if 'issue_number' in data:
            issue = repository.get_issue(number=int(data['issue_number']))
            issue_obj, ctd = GitIssue.objects.get_or_create(
                user=user,
                repository=repository_obj,
                github_id=issue.id
            )
            issue_obj.lamports = int(data['lamports'])
            issue_obj.title = issue.title
            issue_obj.body = issue.body
            issue_obj.pda = data['pda']
            
            source_branch = 'main'
            target_branch = 'bounty-'+slugify(issue.title)+'-'+str(issue.id)

            issue_obj.branch_name = target_branch
            issue_obj.save()
            sb = repository.get_branch(source_branch)
            repository.create_git_ref(ref='refs/heads/' + target_branch, sha=sb.commit.sha)
            # CREATED BRANCH ^

            return {'github_issue_id':issue.id,'title': issue.title, 'body':issue.body, 'github_repository_id':repository.id,'internal_issue_id':issue_obj.id,'lamports':issue_obj.lamports,'minimum_date':issue_obj.minimum_date, 'pda':issue_obj.pda}
        else:
            pass
            # title = data['title']
            # body = data['body']
            # issue = repository.create_issue(title=title, body=body)
            # issue_obj, ctd = GitIssue.objects.get_or_create(
            #     user=user,
            #     repository=repository_obj,
            #     github_id=issue.id
            # )
            # issue_obj.lamports = int(data['lamports'])
            # issue_obj.save()
            # return {'github_issue_id':issue.id,'title': issue.title, 'body':issue.body, 'github_repository_id':repository.id,'internal_issue_id':issue_obj.id,'lamports':issue_obj.lamports,'minimum_date':issue_obj.minimum_date, 'pda':issue_obj.pda}
    return []


def apply_issue(user, data):
    access_token = get_access_token(user)
    if access_token:
        github_issue_id = data['github_issue_id']
        issue = GitIssue.objects.get(github_id=int(github_issue_id))
        bounty_hunter, _ = BountyHunter.objects.get_or_create(
            user=user,
            issue=issue,
        )
        bounty_hunter.wallet = data['wallet']
        bounty_hunter.save()

        return bounty_hunter
        