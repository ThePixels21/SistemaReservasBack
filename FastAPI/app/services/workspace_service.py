from peewee import DoesNotExist

from FastAPI.app.database import WorkspaceModel, ScheduleModel
from FastAPI.app.models.workspace import Workspace

from fastapi import Body

class WorkspaceService:

    def get_workspaces(self):
        """
        Get all workspaces, including their schedules.
        """
        workspaces = WorkspaceModel.select().dicts()
        results = []

        for workspace in workspaces:
            schedules = ScheduleModel.select().where(ScheduleModel.workspace == workspace['id']).dicts()
            workspace['schedules'] = list(schedules)
            results.append(workspace)

        return results

    def get_workspace(self, workspace_id: int):
        """
        Get a specific workspace along with its schedules.
        """
        try:
            workspace = WorkspaceModel.get(WorkspaceModel.id == workspace_id)
            schedules = ScheduleModel.select().where(ScheduleModel.workspace == workspace_id).dicts()
            return {**workspace.__data__, 'schedules': list(schedules)}
        except DoesNotExist:
            return "Workspace not found"

    def create_workspace(self, workspace: Workspace = Body(...)):
        """
        Create a new workspace.
        """
        WorkspaceModel.create(
            id=workspace.id,
            type=workspace.type.value,
            capacity=workspace.capacity,
            hourlyRate=workspace.hourlyRate,
            created_by=workspace.createdBy
        )
        return workspace

    def update_workspace(self, workspace_id: int, workspace_data: dict):
        """
        Update an existing workspace.
        """
        WorkspaceModel.update(workspace_data).where(WorkspaceModel.id == workspace_id).execute()
        return "Workspace updated successfully"

    def delete_workspace(self, workspace_id: int):
        """
        Delete a workspace and its schedules.
        """
        try:
            workspace = WorkspaceModel.get(WorkspaceModel.id == workspace_id)
            workspace.delete_instance()
            return "Workspace and related schedules deleted successfully"
        except DoesNotExist:
            return "Workspace not found"

    def add_schedule(self, workspace_id: int, schedule_data: dict):
        """
        Add a new schedule to a workspace.
        """
        try:
            workspace = WorkspaceModel.get(WorkspaceModel.id == workspace_id)
            ScheduleModel.create(
                openingTime=schedule_data['openingTime'],
                closingTime=schedule_data['closingTime'],
                status=schedule_data['status'],
                workspace=workspace
            )
            return "Schedule added successfully"
        except DoesNotExist:
            return "Workspace not found"

    def delete_schedule(self, schedule_id: int):
        """
        Delete a specific schedule by ID.
        """
        try:
            schedule = ScheduleModel.get(ScheduleModel.id == schedule_id)
            schedule.delete_instance()
            return "Schedule deleted successfully"
        except DoesNotExist:
            return "Schedule not found"