USE [Taxsale2024]
GO
/****** Object:  Table [dbo].[vg_ActivityBaseTable]    Script Date: 3/31/2025 3:44:47 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[vg_ActivityBaseTable](
	[ActivityID] [int] IDENTITY(1,1) NOT NULL,
	[ActivityTypeID] [int] NOT NULL,
	[UserGuid] [uniqueidentifier] NOT NULL,
	[ActivityDateTime] [smalldatetime] NOT NULL,
	[Status] [bit] NOT NULL,
	[VGProductID] [int] NOT NULL,
 CONSTRAINT [PK_vg_ActivityBaseTable] PRIMARY KEY CLUSTERED 
(
	[ActivityID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [dbo].[vg_ActivityBaseTable] ADD  CONSTRAINT [DF_vg_ActivityBaseTable_ActivityDateTime]  DEFAULT (getdate()) FOR [ActivityDateTime]
GO
ALTER TABLE [dbo].[vg_ActivityBaseTable]  WITH CHECK ADD  CONSTRAINT [FK_vg_ActivityBaseTable_aspnet_Users] FOREIGN KEY([UserGuid])
REFERENCES [dbo].[aspnet_Users] ([UserId])
GO
ALTER TABLE [dbo].[vg_ActivityBaseTable] CHECK CONSTRAINT [FK_vg_ActivityBaseTable_aspnet_Users]
GO
ALTER TABLE [dbo].[vg_ActivityBaseTable]  WITH CHECK ADD  CONSTRAINT [FK_vg_ActivityBaseTable_vg_ActivityTypes] FOREIGN KEY([ActivityTypeID])
REFERENCES [dbo].[vg_ActivityTypes] ([ActivityTypeID])
GO
ALTER TABLE [dbo].[vg_ActivityBaseTable] CHECK CONSTRAINT [FK_vg_ActivityBaseTable_vg_ActivityTypes]
GO
