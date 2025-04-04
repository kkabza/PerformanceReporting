USE [Taxsale2024]
GO
/****** Object:  Table [dbo].[vg_ActivityLog]    Script Date: 3/31/2025 3:44:47 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[vg_ActivityLog](
	[ActivityID] [int] IDENTITY(1,1) NOT NULL,
	[ActivityDate] [datetime] NOT NULL,
	[UserID] [uniqueidentifier] NOT NULL,
	[ActivityName] [varchar](50) NOT NULL,
	[ActivityDetails] [varchar](50) NULL
) ON [PRIMARY]
GO
